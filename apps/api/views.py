from rest_framework.decorators import (
    parser_classes,
    permission_classes,
    api_view)
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny)
from rest_framework.parsers import (
    MultiPartParser,
    FileUploadParser,
    FormParser
)
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
    HTTP_200_OK)
from rest_framework.authtoken.models import Token

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.shortcuts import (
    get_object_or_404,
    get_list_or_404)
from django.db.models import Q, Count
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from .paginations import *
from apps.accounts.models import *
from apps.center.models import *
from apps.course.models import *
from apps.accounts.serializers import *
from apps.center.serializers import *
from apps.course.serializers import *


@csrf_exempt
@api_view(["post"])
def SigninAPI(request):
    useremail = request.data.get("email")
    userpassword = request.data.get("password")

    if useremail is None or userpassword is None:
        return Response({
            'error': True,
        }, status=HTTP_400_BAD_REQUEST)

    user = authenticate(email=useremail, password=userpassword)
    if not user:
        return Response({
            'error': True,
            'response': _('user email or password is wrong')
        }, status=HTTP_404_NOT_FOUND)
    return Response({
        'error': False,
        'data': MemberSerializers(user).data,
        'token': TokenSerializer(create_token(user)).data,
        'code': code,
    }, status=HTTP_200_OK)


def create_token(user):
    Token.objects.filter(user=user).delete()
    return Token.objects.create(user=user)


@csrf_exempt
@api_view(["post"])
def SignupAPI(request):
    serializer = MemberSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        return Response({
            'error': False,
            'data': _('account created, login next')
        }, status=HTTP_200_OK)


class UpdatePassWordAPI(UpdateAPIView):
    serializer_class = UpdatePassWordSerializers
    model = Member
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = self.request.user
        return obj

    @csrf_exempt
    def update(self, request):
        self.object = self.get_object()
        serializer = UpdatePassWordSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if self.object.check_password(serializer.data.get("old_password")):
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                return Response(data={'data': _('password updated successfully')}, status=HTTP_200_OK)
            else:
                return Response(data={'data': _('old password is invalid')}, status=HTTP_400_BAD_REQUEST)


class ResetPasswordAPI(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UpdatePassWordSerializers
    model = Member

    def get_object(self):
        obj = get_object_or_404(Member, email=self.request.data['email'])
        return obj

    @csrf_exempt
    def update(self, request):
        self.object = self.get_object()
        serializer = UpdatePassWordSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.object.set_password(serializer.data.get("confirm_password"))
            self.object.save()
            return Response(data={'data': _('password updated successfully')}, status=HTTP_200_OK)


@csrf_exempt
@api_view(['get'])
def CategoryAPI(request):
    course_categories = Course._meta.get_field('category').choices
    context = []
    for categorty in course_categories:
        context.append({'pk': categorty[0], 'categorty': categorty[1]})
    return Response({'data': context}, status=HTTP_200_OK)


class ListCourseAPI(ListAPIView):
    serializer_class = CourseSerializers
    pagination_class = CoursePaginatorAPI

    def get_queryset(self):
        return Course.objects.annotate(
            view=Count('courseview')
        ).order_by(
            '-view', 'add_date'
        ).all()


class ListCourseByCategoryAPI(ListAPIView):
    serializer_class = CourseSerializers
    pagination_class = CoursePaginatorAPI

    def get_queryset(self):
        return Course.objects.annotate(
            view=Count('courseview')
        ).order_by(
            '-view', 'add_date'
        ).filter(
            category=self.kwargs['pk']
        )


class ListTrainingCentersAPI(ListAPIView):
    serializer_class = CenterSerializers
    pagination_class = CentersViewPaginationAPI

    def get_queryset(self):
        return Center.objects.all().order_by('add_date')


class SearchCourseAPI(ListAPIView):
    serializer_class = CourseSerializers
    pagination_class = CoursePaginatorAPI
    search_fields = ['name', 'trainee', 'center__name']
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        return Course.objects.annotate(
            view=Count('courseview')
        ).order_by(
            '-view', 'add_date'
        ).all()


@permission_classes([IsAuthenticated])
class LecturesAPI(ListAPIView):
    serializer_class = LectureSerializers
    pagination_class = LecturePaginatorAPI

    def get_queryset(self):
        return Lecture.objects.filter(course=self.kwargs['pk']).order_by('pk')


@permission_classes([IsAuthenticated])
@csrf_exempt
@api_view(['get'])
def LectureAPI(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk)
    LectureAttend.objects.get_or_create(lecture=lecture, account=request.user)
    return Response(
        {
            'data': LectureSerializers(lecture).data,
            'attend': LectureAttend.objects.filter(lecture__course=lecture.course, account=request.user).count()
        },
        status=HTTP_200_OK
    )


@permission_classes([IsAuthenticated])
@csrf_exempt
@api_view(['get'])
def LecturesAttendAPI(request, pk, apk):
    course = get_object_or_404(Course, pk=pk)
    attend = LectureAttend.objects.filter(lecture__course=course, account=pk).count()
    return Response(
        {'attend': attend, 'lectures': course.lectures},
        status=HTTP_200_OK
    )


@permission_classes([IsAuthenticated])
@csrf_exempt
@api_view(["post"])
def RateCourseAPI(request):
    query = CourseRate.objects.filter(
        course=Course.objects.get(pk=request.data.get("course")), account=Member.objects.get(pk=request.data.get("member"))
    )
    if not query:
        serializer = CourseRateSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'error': False}, status=HTTP_201_CREATED)
        else:
            return Response({'error': True}, status=HTTP_400_BAD_REQUEST)
    else:
        query.update(rate=request.data.get("rate"))
        return Response({'error': False}, status=HTTP_200_OK)



@permission_classes([IsAuthenticated])
class AccessedCoursesAPI(ListAPIView):
    serializer_class = CourseSerializers
    pagination_class = CoursePaginatorAPI

    def get_queryset(self):
        accesses = list(
            CoursePayment.objects.filter(
                account__pk=self.request.user.pk, allow_access=True
            ).values_list('course', flat=True)
        )
        return Course.objects.filter(coursepayment__in=accesses).order_by('pk')


@permission_classes([IsAuthenticated])
class RequestedCoursesAPI(ListAPIView):
    serializer_class = CourseSerializers
    pagination_class = CoursePaginatorAPI

    def get_queryset(self):
        accesses = list(
            CoursePayment.objects.filter(
                account__pk=self.request.user.pk, allow_access=False
            ).values_list('course', flat=True)
        )
        return Course.objects.filter(coursepayment__in=accesses).order_by('pk')


@permission_classes([IsAuthenticated])
class SearchAccessedCoursesAPI(ListAPIView):
    serializer_class = CourseSerializers
    pagination_class = CoursePaginatorAPI
    search_fields = ['name', 'trainee', 'center__name']
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        accesses = list(
            CoursePayment.objects.filter(
                account__pk=self.request.user.pk, allow_access=True
            ).values_list('course', flat=True)
        )
        return Course.objects.filter(coursepayment__in=accesses).order_by('pk')


@permission_classes([IsAuthenticated])
class SearchRequestedCoursesAPI(ListAPIView):
    serializer_class = CourseSerializers
    pagination_class = CoursePaginatorAPI
    search_fields = ['name', 'trainee', 'center__name']
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        accesses = list(
            CoursePayment.objects.filter(
                account__pk=self.request.user.pk, allow_access=False
            ).values_list('course', flat=True)
        )
        return Course.objects.filter(coursepayment__in=accesses).order_by('pk')


class CourseCommentsAPI(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseCommentSerializers
    pagination_class = CourseCommentPaginatorAPI

    @csrf_exempt
    def get_queryset(self):
        return CourseComment.objects.filter(course__pk=self.kwargs['pk']).order_by('add_date')


@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
@csrf_exempt
@api_view(['post'])
def CoursePaymentAPI(request, pk):
    serializer = CoursePaymentSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(
            course=Course.objects.get(pk=pk),
            account=request.user
        )
        return Response(
            {
                'error': False,
                'data': _('payment done, our team will contact you soon')
            },
            status=HTTP_200_OK
        )


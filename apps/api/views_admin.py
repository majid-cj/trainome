from rest_framework.decorators import (
    permission_classes,
    api_view,
    parser_classes)
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated)
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import filters
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
    HTTP_200_OK)
from rest_framework.authtoken.models import Token

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.db.models import Q, Count
from django.shortcuts import (
    get_object_or_404,
    get_list_or_404)
from django.utils.translation import gettext_lazy as _


from .paginations import *
from apps.home.models import *
from apps.accounts.models import *
from apps.home.serializers import *
from apps.accounts.serializers import *


@permission_classes((IsAdminUser,))
@parser_classes((MultiPartParser,))
@csrf_exempt
@api_view(["post"])
def AddHomeMenuAPI(request):
    serializer = HomeMenuAPISerializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({
            'error': False,
            'data': _('menu created')
        }, status=HTTP_200_OK)
    return Response({
        'error': True,
        'data': _('error occured')
    }, status=HTTP_400_BAD_REQUEST)


@permission_classes((IsAdminUser,))
@csrf_exempt
@api_view(["post"])
def AddHomeMenuPermissionAPI(request):
    menu = get_object_or_404(HomeMenu, pk=request.data.get("menu"))
    try:
        HomeMenuPermission.objects.create(member_type=request.data.get("type"), menu=menu)
        return Response({
            'error': False,
            'data': _('permission created')
        }, status=HTTP_200_OK)
    except IntegrityError as e:
        if 'UNIQUE constraint' in '{}'.format(e):
            return Response({
                'error': True,
                'data': _('this menu is already created')
            }, status=HTTP_400_BAD_REQUEST)
        return Response({
            'error': True,
            'data': _('error occured')}, status=HTTP_400_BAD_REQUEST)


@permission_classes((IsAdminUser,))
@csrf_exempt
@api_view(["delete"])
def DeleteHomeMenuPermissionAPI(request):
    if HomeMenuPermission\
        .objects\
        .filter(member_type=request.data.get("type"), menu__pk=request.data.get("menu"))\
            .delete():
        return Response({
            'error': False,
            'data': _('permission delete')
        }, status=HTTP_200_OK)
    return Response({
        'error': True,
        'data': _('error occured')
    }, status=HTTP_400_BAD_REQUEST)


@permission_classes((IsAdminUser,))
@csrf_exempt
@api_view(["get"])
def GetHomeMenuAPI(request):
    menus = get_list_or_404(HomeMenu.objects.order_by('menu_priority'))
    return Response({
        'data': HomeMenuAPISerializers(menus, many=True).data
    }, status=HTTP_200_OK)


@permission_classes((IsAdminUser,))
@csrf_exempt
@api_view(["delete"])
def DeleteMenuAPI(request, pk):
    menus = get_object_or_404(HomeMenu, pk=pk)
    menus.delete()
    return Response({
        'error': False,
        'data': _('menu delete')
    }, status=HTTP_200_OK)


@permission_classes((IsAdminUser,))
@csrf_exempt
@api_view(["get"])
def GetMemberTypesAPI(request, pk):
    hmp_query = HomeMenuPermission.objects.filter(menu__pk=pk)
    mt_query = Member._meta.get_field('member_type').choices
    context = []
    for types in mt_query:
        if types[0] in [x.member_type for x in hmp_query]:
            context.append({'pk': types[0], 'type_name': types[1], 'permission': 1})
        else:
            context.append({'pk': types[0], 'type_name': types[1], 'permission': None})
    return Response({'data': context}, status=HTTP_200_OK)


@permission_classes((IsAuthenticated,))
@csrf_exempt
@api_view(["get"])
def GetHomeMenuPermissionAPI(request):
    permissions = get_list_or_404(HomeMenuPermission.objects.order_by('menu__menu_priority'),
                                  member_type=request.user.member_type)
    return Response({
        'data': HomeMenuPermissionAPISerializers(permissions, many=True).data
    }, status=HTTP_200_OK)


@permission_classes((IsAdminUser,))
class GetMembersAPI(ListAPIView):
    serializer_class = MemberAPISerializers
    pagination_class = MemberViewPaginationAPI

    def get_queryset(self):
        return Member.objects.all().order_by('created_date')


class SearchMembersAPI(ListAPIView):
    serializer_class = MemberAPISerializers
    pagination_class = MemberViewPaginationAPI
    search_fields = ['email', 'name']
    filter_backends = (filters.SearchFilter,)
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Member.objects.all().order_by('created_date')


class GetMembersByTypeAPI(ListAPIView):
    serializer_class = MemberAPISerializers
    pagination_class = MemberViewPaginationAPI
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Member.objects.filter(member_type=self.kwargs.get("pk")).order_by('created_date')

from rest_framework.pagination import PageNumberPagination



class MemberViewPaginationAPI(PageNumberPagination):
    page_size = 10


class CentersViewPaginationAPI(PageNumberPagination):
    page_size = 6


class CoursePaginatorAPI(PageNumberPagination):
    page_size = 6


class LecturePaginatorAPI(PageNumberPagination):
    page_size = 15


class CourseCommentPaginatorAPI(PageNumberPagination):
    page_size = 25
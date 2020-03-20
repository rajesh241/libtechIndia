"""Default Pagination class application to all APIs"""
from rest_framework import pagination



class LibtechAPIPagination(pagination.LimitOffsetPagination): #PageNumberPagination):
    """Default Pagination class"""
    #page_size   =  20
    default_limit = 50
    max_limit = 10000
    #limit_query_param = 'lim'

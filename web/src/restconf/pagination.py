from rest_framework import pagination



class LibtechAPIPagination(pagination.LimitOffsetPagination): #PageNumberPagination):
    #page_size   =  20
    default_limit   = 5
    max_limit       = 10000
    #limit_query_param = 'lim'

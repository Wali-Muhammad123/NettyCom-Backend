from rest_framework.pagination import PageNumberPagination
class TeamSalesPaginater(PageNumberPagination):
    page_size=10
    page_size_query_param='pageSize'
    max_page_size=25

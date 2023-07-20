from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """
    Custom pagination class that uses the `limit` query parameter to specify
    the page size.
    """

    page_size_query_param = 'limit'

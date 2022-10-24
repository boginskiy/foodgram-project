from rest_framework.pagination import PageNumberPagination


class UserListPagination(PageNumberPagination):
    """Кастомный паджинатор с назначенными параметрами."""

    page_size = 6
    page_size_query_param = 'limit'
    max_page_size = 250

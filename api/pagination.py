from rest_framework.pagination import PageNumberPagination
from meme_generator.settings import DEFAULT_PAGE_SIZE


class LimitPagination(PageNumberPagination):

    page_size_query_param = 'limit'
    page_size = DEFAULT_PAGE_SIZE

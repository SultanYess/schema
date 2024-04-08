from rest_framework import pagination as drf_pagination, response as drf_response
from rest_framework.utils.urls import remove_query_param, replace_query_param


class ContentPaginator(drf_pagination.PageNumberPagination):
    """Пагинатор для контента."""

    page_size = 15
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_next_page(self):
        return self.page.next_page_number() if self.page.has_next() else None

    def get_previous_page(self):
        return self.page.previous_page_number() if self.page.has_previous() else None

    def get_paginated_response(self, data):
        return drf_response.Response(
            {
                "page": {
                    "next": self.get_next_page(),
                    "previous": self.get_previous_page(),
                    "current": self.page.number,
                    "total": self.page.paginator.num_pages,
                },
                "count": self.page.paginator.count,
                "results": data,
            }
        )

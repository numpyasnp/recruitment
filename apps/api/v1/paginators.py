from rest_framework.pagination import PageNumberPagination


class BasePaginator(PageNumberPagination):
    """
    Custom paginator for job postings. Sets page size to 5 and allows client to override with ?page_size=5.
    """

    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 50


class JobPostingPaginator(BasePaginator): ...

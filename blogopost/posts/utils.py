from django.core.paginator import Paginator

from .constants import POSTS_LIMITATION


def make_pages(request, obj):
    paginator = Paginator(obj, POSTS_LIMITATION)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)

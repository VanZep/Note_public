from django.core.paginator import Paginator

from .constants import NUMBER_OF_POSTS


def page_object(request, post_list):
    paginator = Paginator(post_list, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')

    return paginator.get_page(page_number)

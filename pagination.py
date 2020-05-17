from django import template
from django.conf import settings 

register = template.Library()

DISPLAY_PER_PAGE = PRIVATE_DIR = getattr(settings, 'PAGENATE_DISPLAY_PER_PAGE', 7)


@register.simple_tag
def url_replace(request, field, value):
    """

    Args:
        request:
        field:
        value:

    Returns:

    """
    url_dict = request.GET.copy()
    url_dict[field] = str(value)
    return "?" + url_dict.urlencode()


display_per_page = DISPLAY_PER_PAGE
omission_threshold = display_per_page-int(display_per_page/2)


@register.simple_tag
def is_show_omission(max_page):
    """

    Args:
        max_page:

    Returns:

    """
    return max_page > display_per_page


def is_first_omission(current_page):
    """

    Args:
        current_page:

    Returns:

    """
    return current_page > omission_threshold


def is_last_omission(current_page, max_page):
    """

    Args:
        current_page:
        max_page:

    Returns:

    """
    return not max_page < current_page + omission_threshold


@register.simple_tag
def is_show_pager_first(current_page, max_page):
    """

    Args:
        current_page:
        max_page:

    Returns:

    """
    return is_show_omission(max_page) \
        and is_first_omission(current_page)


@register.simple_tag
def is_show_pager_last(current_page, max_page):
    """

    Args:
        current_page:
        max_page:

    Returns:

    """
    return is_show_omission(max_page) \
        and is_last_omission(current_page, max_page)


@register.simple_tag
def get_around_pages(current_page, max_page):
    """

    Args:
        current_page:
        max_page:

    Returns:

    """
    show_list = []
    if is_show_omission(max_page):
        if not is_first_omission(current_page):
            for num in range(display_per_page):
                show_list.append(num+1)
            del show_list[display_per_page-1]
        elif not is_last_omission(current_page, max_page):
            for num in range(display_per_page):
                show_list.append(max_page-num)
            del show_list[display_per_page-1]
        else:
            for index in range(int((display_per_page-2)/2)):
                num = index + 1
                show_list.append(current_page+num)
                show_list.append(current_page-num)
            show_list.append(current_page)
    else:
        for num in range(max_page):
            show_list.append(num+1)
    show_list.sort()
    return show_list

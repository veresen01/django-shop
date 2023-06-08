from django.http import HttpRequest


def is_ajax(request: HttpRequest) -> bool:
    """
    Метод проверяет тип request на ajax
    :param request:
    :return:
    """
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'

from django.shortcuts import render

def page_not_found(request, exception):
    """Ошибка 404: страница не найдена."""

    return render(request, 'core/404.html', {'path': request.path}, status=404)


def csrf_failure(request, reason=''):
    """403: ошибка проверки CSRF, запрос отклонён."""

    return render(request, 'core/403csrf.html')

from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    """Класс об авторе."""

    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    """Класс технологии."""

    template_name = 'about/tech.html'

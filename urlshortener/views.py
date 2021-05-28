from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, CreateView, RedirectView
from urlshortener.models import Link

""" Co mi się nie podoba:
    - Jak link już został skrócony to rzuca błąd walidacji, a powinno dać link który już mamy w bazie[*]
    - Jak wpiszemy zły shortened url to dostajemy 404, powinno być chyba że np przekierwouje na homepage
     i pisze ze nie ma takiego linka
    - ListView jest chyba niepotrzebne, bo jest wzmianka tylko o adminie[*]
    - Można usunąc forma jeżeli korzystam z createview dla modelu[*]
    - Brak testów[*]
    - Użytkownik powinien dostać pełen skrócony link a nie tylko tą końcówke[*]
    https://studygyaan.com/django/django-everywhere-host-your-django-app-for-free-on-heroku
    https://www.youtube.com/watch?v=Q_YOYNiSVDY
"""


class LinkCreateView(CreateView):
    model = Link
    fields = ("full_path",)

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, 'urlshortener/show-link.html', {'shortened_link': self.object.short_path})

    def form_invalid(self, form):
        full_path = form.data['full_path']
        if link := self.get_link_if_already_exists(full_path):
            return render(self.request, 'urlshortener/show-link.html', {'shortened_link': link.short_path})
        else:
            super(LinkCreateView, self).form_invalid(form)

    def get_link_if_already_exists(self, full_path):
        link = self.model.objects.filter(full_path=full_path).first()
        return link


class LinkRedirect(RedirectView):
    permanent = True
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        link = get_object_or_404(Link, short_path=kwargs['short_path'])
        return link.full_path

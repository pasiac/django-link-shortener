from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, RedirectView
from urlshortener.models import Link, UpdateProhibitedException


class LinkCreateView(CreateView):
    model = Link
    fields = ("full_path",)

    def form_valid(self, form):
        try:
            self.object = form.save()
        except UpdateProhibitedException:
            return render(self.request, 'urlshortener/show-link.html',
                          {'shortened_link': "Updating fields is prohibited."})
        return render(self.request, 'urlshortener/show-link.html', {'shortened_link': self.object.short_path})

    def form_invalid(self, form):
        full_path = form.data['full_path']
        if link := self.get_link_if_already_exists(full_path):
            return render(self.request, 'urlshortener/show-link.html', {'shortened_link': link.short_path})
        else:
            return super(LinkCreateView, self).form_invalid(form)

    def get_link_if_already_exists(self, full_path):
        link = self.model.objects.filter(full_path=full_path).first()
        return link


class LinkRedirect(RedirectView):
    permanent = True
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        link = get_object_or_404(Link, short_path=kwargs['short_path'])
        return link.full_path

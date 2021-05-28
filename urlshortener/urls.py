from django.urls import path

from urlshortener.views import LinkCreateView, LinkRedirect

urlpatterns = [
    path("", LinkCreateView.as_view(), name="create_link"),
    path("<str:short_path>", LinkRedirect.as_view(), name="link-redirect"),
]
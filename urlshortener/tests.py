from django.test import TestCase
from django.urls import reverse

from urlshortener.models import Link

STATUS_CODE_CREATED = 201
STATUS_CODE_REDIRECTED = 301
STATUS_CODE_NOT_FOUND = 404


class TestRedirect(TestCase):
    def setUp(self) -> None:
        self.link = Link.objects.create(full_path="https://docs.djangoproject.com/")

    def test_short_path_redirects(self):
        url = reverse('link-redirect', args=[self.link.short_path])
        response = self.client.get(url)
        self.assertEqual(response.status_code, STATUS_CODE_REDIRECTED)

    def test_short_path_redirects_to_full_path_destination(self):
        url = reverse('link-redirect', args=[self.link.short_path])
        response = self.client.get(url)
        self.assertEqual(response.get('location'), self.link.full_path)

    def test_invalid_short_path_response_status_code_equal_not_found(self):
        url = reverse('link-redirect', args=['invalid_shortened_path'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, STATUS_CODE_NOT_FOUND)


class TestCreate(TestCase):
    def setUp(self) -> None:
        self.existing_link = Link.objects.create(full_path="https://docs.djangoproject.com/")
        self.non_existing_full_path = "https://docs.python.org/"

    def test_create_link_with_non_existing_full_path_returns_status_code_created(self):
        url = reverse('create_link')
        response = self.client.post(url, data={'full_path': self.non_existing_full_path})
        self.assertEqual(response.status_code, 200)

    def test_create_link_with_non_existing_full_path_creates_link_object(self):
        url = reverse('create_link')
        self.client.post(url, data={'full_path': self.non_existing_full_path})
        created_object = Link.objects.filter(full_path=self.non_existing_full_path).exists()
        self.assertTrue(created_object)

    def test_create_link_returns_shortened_path(self):
        url = reverse('create_link')
        response = self.client.post(url, data={'full_path': self.non_existing_full_path})
        created_object = Link.objects.get(full_path=self.non_existing_full_path)
        self.assertContains(response, created_object.short_path)

    def test_create_link_with_existing_full_path_returns_shortened_path(self):
        url = reverse('create_link')
        existing_full_path = self.existing_link.full_path
        response = self.client.post(url, data={'full_path': existing_full_path})
        existing_object = Link.objects.get(full_path=existing_full_path)
        self.assertContains(response, existing_object.short_path)

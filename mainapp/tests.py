import pickle
from http import HTTPStatus
from unittest import mock

from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail as django_mail

from authapp.models import User
from mainapp import tasks
from mainapp.models import News, Courses


class StaticPagesSmokeTest(TestCase):
    def test_index_page_open(self):
        url = reverse("mainapp:index")
        result = self.client.get(url)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_contacts_page_open(self):
        url = reverse("mainapp:contacts")
        result = self.client.get(url)
        self.assertEqual(result.status_code, HTTPStatus.OK)


class NewsTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        for i in range(10):
            News.objects.create(
                title=f'title{i}',
                preambule=f'preambule{i}',
                body=f'body{i}'
            )
        User.objects.create_superuser(username='django', password='geekbrains')
        self.client_with_auth = Client()
        auth_url = reverse('authapp:login')
        self.client_with_auth.post(
            auth_url,
            {'username': 'django', 'password': 'geekbrains'}
        )

    def test_open_page(self):
        url = reverse("mainapp:news")
        result = self.client.get(url)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_open_crete_deny_access(self):
        path = reverse("mainapp:news_create")
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_page_open_crete_by_admin(self):
        path = reverse("mainapp:news_create")
        result = self.client_with_auth.post(
            path,
            data={'title': 'test title', 'preambule': 'test preambule', 'body': 'test body'}
        )
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_page_open_update_deny_access(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_update", args=[news_obj.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_page_open_update_by_admin(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_update", args=[news_obj.pk])
        result = self.client_with_auth.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_delete_deny_access(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_delete", args=[news_obj.pk])
        result = self.client.post(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_delete_by_admin(self):
        news_obj = News.objects.first()
        path = reverse("mainapp:news_delete", args=[news_obj.pk])
        self.client_with_auth.post(path)
        news_obj.refresh_from_db()
        self.assertTrue(news_obj.deleted)


class TestTaskMailSend(TestCase):
    def test_mail_send(self):
        message_text = "test_message_text"
        tasks.send_feedback_mail(message_text)
        self.assertEqual(django_mail.outbox[0].body, message_text)


class TestCoursesWithMock(TestCase):


    fixtures = (
        "authapp/fixtures/001_user_admin.json",
        "mainapp/fixtures/002_courses.json",
        "mainapp/fixtures/003_lessons.json",
        "mainapp/fixtures/004_teachers.json",
    )


def test_page_open_detail(self):
    course_obj = Courses.objects.get(pk=161)
    path = reverse("mainapp:courses_detail", args=[course_obj.pk])
    with open("mainapp/fixtures/006_feedback_list_2.bin", "rb") as inpf, mock.patch("django.core.cache.cache.get") as mocked_cache:
        mocked_cache.return_value = pickle.load(inpf)
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)
        self.assertTrue(mocked_cache.called)

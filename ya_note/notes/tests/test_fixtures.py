from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.not_author = User.objects.create(username='Читатель')
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)
        cls.note = Note.objects.create(title='Заголовок',
                                       text='Текст',
                                       slug='Slug',
                                       author=cls.author)

        cls.LOGIN_URL_REVERSE = reverse('users:login')
        cls.LOGOUT_URL_REVERSE = reverse('users:logout')
        cls.SIGNUP_URL_REVERSE = reverse('users:signup')
        cls.HOME_URL_REVERSE = reverse('notes:home')
        cls.NOTES_URL_REVERSE = reverse('notes:list')
        cls.DETAIL_URL_REVERSE = reverse('notes:detail', args=(cls.note.slug,))
        cls.NOTE_ADD_URL_REVERSE = reverse('notes:add')
        cls.EDIT_URL_REVERSE = reverse('notes:edit', args=(cls.note.slug,))
        cls.DELETE_URL_REVERSE = reverse('notes:delete', args=(cls.note.slug,))
        cls.SUCCESS_URL_REVERSE = reverse('notes:success')

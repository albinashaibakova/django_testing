from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note


User = get_user_model()


class TestNoteListPage(TestCase):

    HOME_URL = reverse('notes:list')
    NOTE_ADD_URL = reverse('notes:add')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.not_author = User.objects.create(username='Не автор')
        cls.note = Note.objects.create(title='Заметка',
                                       text='Текст заметки',
                                       slug='slug',
                                       author=cls.author)

    def test_note_in_list_for_author(self):
        self.client.force_login(self.author)
        response = self.client.get(self.HOME_URL)
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    def test_note_in_list_for_not_author(self):
        self.client.force_login(self.not_author)
        response = self.client.get(self.HOME_URL)
        object_list = response.context['object_list']
        self.assertNotIn(self.note, object_list)

    def test_create_note_page_contains_form(self):
        self.client.force_login(self.author)
        response = self.client.get(self.NOTE_ADD_URL)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_edit_note_page_contains_form(self):
        self.client.force_login(self.author)
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

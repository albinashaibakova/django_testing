from http import HTTPStatus

import django.contrib.auth
from django.contrib.auth import get_user_model
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .test_fixtures import BaseTestCase


User = get_user_model()


class TestNoteCreation(BaseTestCase):
    TITLE = 'Заголовок заметки'
    TEXT = 'Текст заметки'
    SLUG = 'Slug'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.form_data = {'title': cls.TITLE,
                         'text': cls.TEXT,
                         'slug': cls.SLUG}

    def test_user_can_create_note(self):
        Note.objects.all().delete()
        response = self.auth_client.post(self.NOTE_ADD_URL_REVERSE,
                                         data=self.form_data)
        self.assertRedirects(response, self.SUCCESS_URL_REVERSE)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author,
                         django.contrib.auth.get_user(self.auth_client))

    def test_anonymous_user_cant_create_note(self):
        Note.objects.all().delete()
        response = self.client.post(self.NOTE_ADD_URL_REVERSE,
                                    data=self.form_data)
        expected_url = (f'{self.LOGIN_URL_REVERSE}?'
                        f'next={self.NOTE_ADD_URL_REVERSE}')
        self.assertRedirects(response, expected_url)
        self.assertEqual(Note.objects.count(), 0)

    def test_not_unique_slug(self):
        Note.objects.all().delete()
        self.auth_client.post(self.NOTE_ADD_URL_REVERSE,
                              data=self.form_data)
        self.form_data['slug'] = self.SLUG
        response = self.auth_client.post(self.NOTE_ADD_URL_REVERSE,
                                         data=self.form_data)
        self.assertEqual(Note.objects.count(), 1)
        self.assertFormError(response,
                             'form', 'slug',
                             errors=(self.SLUG + WARNING))

    def test_empty_slug(self):
        self.form_data.pop('slug')
        Note.objects.all().delete()
        response = self.auth_client.post(self.NOTE_ADD_URL_REVERSE,
                                         data=self.form_data)
        self.assertRedirects(response, self.SUCCESS_URL_REVERSE)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)


class TestNoteEditDelete(BaseTestCase):
    NEW_TEXT = 'Текст после изменений'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.form_data = {'title': cls.note.title,
                         'text': cls.NEW_TEXT,
                         'slug': cls.note.slug,
                         }

    def test_author_can_edit_note(self):
        response = self.auth_client.post(self.EDIT_URL_REVERSE,
                                         self.form_data)
        self.assertRedirects(response, self.SUCCESS_URL_REVERSE)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.form_data['title'])
        self.assertEqual(self.note.text, self.form_data['text'])
        self.assertEqual(self.note.slug, self.form_data['slug'])
        self.assertEqual(self.note.author,
                         django.contrib.auth.get_user(self.auth_client))

    def test_other_user_cant_edit_note(self):
        response = self.not_author_client.post(self.EDIT_URL_REVERSE,
                                               self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(slug=self.note.slug)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)

    def test_author_can_delete_note(self):
        notes_before_delete = Note.objects.count()
        response = self.auth_client.post(self.DELETE_URL_REVERSE)
        self.assertRedirects(response, self.SUCCESS_URL_REVERSE)
        self.assertEqual(Note.objects.count(),
                         notes_before_delete - 1)

    def test_other_user_cant_delete_note(self):
        notes_before_delete = Note.objects.count()
        response = self.not_author_client.post(self.DELETE_URL_REVERSE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        assert response.status_code == HTTPStatus.NOT_FOUND
        self.assertEqual(Note.objects.count(),
                         notes_before_delete)

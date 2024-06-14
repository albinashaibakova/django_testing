from notes.forms import NoteForm
from .test_fixtures import BaseTestCase


class TestNoteListPage(BaseTestCase):

    def test_note_in_list_for_author(self):
        response = self.auth_client.get(self.NOTES_URL_REVERSE)
        self.assertIn(self.note, response.context['object_list'])

    def test_note_in_list_for_not_author(self):
        response = self.not_author_client.get(self.NOTES_URL_REVERSE)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_create_and_edit_note_page_contains_form(self):
        urls = (
            self.NOTE_ADD_URL_REVERSE,
            self.EDIT_URL_REVERSE,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.auth_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)

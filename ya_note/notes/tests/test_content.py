from notes.forms import NoteForm
from .lib import (
    TestBasicClass,
    NOTES_LIST,
    NOTES_EDIT,
    NOTES_ADD
)


class TestContent(TestBasicClass):

    def test_note_in_list(self):
        response = self.auth_author.get(NOTES_LIST)
        notes = response.context['object_list']
        self.assertIn(self.note, notes)

    def test_note_in_list_author_another(self):
        response = self.auth_reader.get(NOTES_LIST)
        notes = response.context['object_list']
        self.assertNotIn(self.note, notes)

    def test_existing_form(self):
        urls = (
            NOTES_EDIT,
            NOTES_ADD
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.auth_author.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)

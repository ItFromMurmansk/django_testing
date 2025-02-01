from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .lib import (
    TestBasicClass,
    NOTES_ADD,
    NOTES_SUCCESS,
    NOTES_DELETE,
    NOTES_EDIT,
    SLUG
)


FORM_DATA = {
    'title': 'zagolovok',
    'text': 'text',
    'slug': SLUG
}


class TestLogic(TestBasicClass):

    def test_anonymous_user_cant_create_note(self):
        self.client.post(NOTES_ADD, data=FORM_DATA)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.note_count)

    def test_user_can_create_note(self):
        Note.objects.all().delete()
        self.auth_author.post(NOTES_ADD, data=FORM_DATA)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.note_count)
        note_item = Note.objects.get()
        self.assertEqual(note_item.title, FORM_DATA['title'])
        self.assertEqual(note_item.text, FORM_DATA['text'])
        self.assertEqual(note_item.slug, FORM_DATA['slug'])
        self.assertEqual(note_item.author, self.author)

    def test_slug_unique(self):
        note_count = Note.objects.count()
        response = self.auth_author.post(NOTES_ADD, data=FORM_DATA)
        self.assertEqual(note_count, Note.objects.count())
        self.assertFormError(response,
                             form='form',
                             field='slug',
                             errors=FORM_DATA['slug'] + WARNING)

    def test_author_can_delete_note(self):
        self.auth_author.delete(NOTES_DELETE)
        self.assertEqual(self.note_count, Note.objects.count() + 1)

    def test_other_user_cant_delete_note(self):
        self.auth_reader.delete(NOTES_DELETE)
        note_count = Note.objects.count()
        self.assertEqual(note_count, self.note_count)

    def test_empty_slug(self):
        Note.objects.all().delete()
        self.auth_author.post(NOTES_ADD, data={
            'title': 'zagolovok',
            'text': 'text'})
        note_item = Note.objects.get()
        self.assertEqual(note_item.slug, slugify(FORM_DATA['title']))

    def test_author_can_edit_note(self):
        response = self.auth_author.post(NOTES_EDIT, data=FORM_DATA)
        self.assertRedirects(response, NOTES_SUCCESS)
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.text, FORM_DATA['text'])
        self.assertEqual(note.slug, FORM_DATA['slug'])
        self.assertEqual(note.title, FORM_DATA['title'])
        self.assertEqual(note.author, self.note.author)

    def test_other_user_cant_edit_note(self):
        response = self.auth_reader.post(NOTES_EDIT, data=FORM_DATA)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_item = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.text, note_item.text)
        self.assertEqual(self.note.title, note_item.title)
        self.assertEqual(self.note.slug, note_item.slug)
        self.assertEqual(self.note.author, note_item.author)

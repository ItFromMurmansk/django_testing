from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.author_another = User.objects.create(username='Не Лев Толстой')
        cls.auth_one = Client()
        cls.auth_two = Client()
        cls.auth_one.force_login(cls.author)
        cls.auth_two.force_login(cls.author_another)

        cls.note = Note.objects.create(title='Запись 1',
                                       text='Просто текст.',
                                       slug='Note1',
                                       author=cls.author)

    def test_note_in_list(self):
        url = reverse('notes:list')
        response = self.auth_one.get(url)
        notes = response.context['object_list']
        self.assertIn(self.note, notes)

    def test_note_in_list_author_another(self):
        url = reverse('notes:list')
        response = self.auth_two.get(url)
        notes = response.context['object_list']
        self.assertNotIn(self.note, notes)

    def test_existing_form(self):
        urls = (
            reverse('notes:add'),
            reverse('notes:edit', args=(self.note.slug,))
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.auth_one.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)

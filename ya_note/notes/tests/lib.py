from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()

SLUG = 'zagolovok'
NOTES_ADD = reverse('notes:add')
NOTES_DELETE = reverse('notes:delete', args=(SLUG,))
NOTES_DETAIL = reverse('notes:detail', args=(SLUG,))
NOTES_EDIT = reverse('notes:edit', args=(SLUG,))
NOTES_HOME = reverse('notes:home')
NOTES_LIST = reverse('notes:list')
NOTES_SUCCESS = reverse('notes:success')
USERS_LOGIN = reverse('users:login')
USERS_LOGOUT = reverse('users:logout')
USERS_SIGNUP = reverse('users:signup')
REDIRECT = f'{USERS_LOGIN}?next='


class TestBasicClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.reader = User.objects.create(username='Reader')
        cls.auth_author = Client()
        cls.auth_reader = Client()
        cls.auth_author.force_login(cls.author)
        cls.auth_reader.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug=SLUG,
            author=cls.author
        )
        cls.note_count = Note.objects.count()

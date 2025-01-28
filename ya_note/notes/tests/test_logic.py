from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from pytils.translit import slugify

# Импортируем из файла с формами список стоп-слов и предупреждение формы.
# Загляните в news/forms.py, разберитесь с их назначением.
from notes.models import Note
from notes.forms import WARNING

User = get_user_model()


class TestLogic(TestCase):
    # Текст комментария понадобится в нескольких местах кода,
    # поэтому запишем его в атрибуты класса.
    COMMENT_TEXT = 'Текст комментария'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.author_another = User.objects.create(username='Не Лев Толстой')
        cls.auth_one = Client()
        cls.auth_two = Client()
        cls.auth_one.force_login(cls.author)
        cls.auth_two.force_login(cls.author_another)
        cls.form_data = {'title': 'Заголовок',
                         'text': 'Текст',
                         'slug': 'Zametka'}

    def test_anonymous_user_cant_create_note(self):
        # Совершаем запрос от анонимного клиента, в POST-запросе отправляем
        # предварительно подготовленные данные формы с текстом комментария.
        url = reverse('notes:add')
        self.client.post(url, data=self.form_data)
        # Считаем количество комментариев.
        notes_count = Note.objects.count()
        # Ожидаем, что комментариев в базе нет - сравниваем с нулём.
        self.assertEqual(notes_count, 0)

    def test_user_can_create_note(self):
        url = reverse('notes:add')
        # Совершаем запрос через авторизованный клиент.
        self.auth_one.post(url, data=self.form_data)
        # Считаем количество комментариев.
        notes_count = Note.objects.count()
        # Убеждаемся, что есть один комментарий.
        self.assertEqual(notes_count, 1)
        # Получаем объект комментария из базы.
        note_item = Note.objects.get()
        # Проверяем, что все атрибуты комментария совпадают с ожидаемыми.
        self.assertEqual(note_item.title, self.form_data['title'])
        self.assertEqual(note_item.text, self.form_data['text'])
        self.assertEqual(note_item.slug, self.form_data['slug'])
        self.assertEqual(note_item.author, self.author)

    def test_slug_unique(self):
        url = reverse('notes:add')
        self.auth_one.post(url, data=self.form_data)
        note_count = Note.objects.count()
        response = self.auth_one.post(url, data=self.form_data)
        note_item = Note.objects.get()
        self.assertFormError(response,
                             form='form',
                             field='slug',
                             errors=note_item.slug + WARNING)
        self.assertEqual(Note.objects.count(), note_count)

    def test_empty_slug(self):
        self.form_data.pop('slug')
        url = reverse('notes:add')
        self.auth_one.post(url, data=self.form_data)
        test_slug = slugify(self.form_data['title'])
        note_item = Note.objects.get()
        self.assertEqual(test_slug, note_item.slug)

    def test_author_can_delete_note(self):
        url = reverse('notes:add')
        self.auth_one.post(url, data=self.form_data)
        url = reverse('notes:delete', args=(self.form_data['slug'],))
        self.auth_one.delete(url)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 0)

    def test_other_user_cant_delete_note(self):
        url = reverse('notes:add')
        self.auth_one.post(url, data=self.form_data)
        url = reverse('notes:delete', args=(self.form_data['slug'],))
        self.auth_two.delete(url)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)


from datetime import datetime, timedelta

import pytest
from django.test.client import Client

from django.conf import settings
from django.utils import timezone
from django.urls import reverse

from news.models import News, Comment

NEWS_TEXT = 'Текст'
USER_LOGIN = 'users:login'
USER_LOGOUT = 'users:logout'
USER_SIGNUP = 'users:signup'
NEWS_EDIT = 'news:edit'
NEWS_DELETE = 'news:delete'
NEWS_HOME = 'news:home'
NEWS_DETAIL = 'news:detail'


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Author')


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Reader')


@pytest.fixture
def auth_author(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def auth_reader(reader):
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def login():
    return reverse(USER_LOGIN)


@pytest.fixture
def logout():
    return reverse(USER_LOGIN)


@pytest.fixture
def signup():
    return reverse(USER_SIGNUP)


@pytest.fixture
def news_home():
    return reverse(NEWS_HOME)


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок новости',
        text='Текст новости',
    )
    return news


@pytest.fixture
def news_detail(news):
    return reverse(NEWS_DETAIL, args=[news.pk])


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text=NEWS_TEXT
    )
    return comment


@pytest.fixture
def comment_edit(comment):
    return reverse(NEWS_EDIT, args=[comment.pk])


@pytest.fixture
def comment_delete(comment):
    return reverse(NEWS_DELETE, args=[comment.pk])


@pytest.fixture
def redirect_url_edit_comment(login, comment_edit):
    return f'{login}?next={comment_edit}'


@pytest.fixture
def redirect_url_delete_comment(login, comment_delete):
    return f'{login}?next={comment_delete}'


@pytest.fixture
def create_bulk_of_news():
    News.objects.bulk_create(
        News(title=f'News number {index}',
             text='News text',
             date=datetime.today() - timedelta(days=index)
             )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def create_bulk_of_comments(news, author):
    now = timezone.now()
    for index in range(3):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Comment text number {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()

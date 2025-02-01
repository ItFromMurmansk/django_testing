from http import HTTPStatus

import pytest
from django.test.client import Client
from pytest_django.asserts import assertRedirects

from pytest_lazyfixture import lazy_fixture as lf

pytestmark = pytest.mark.django_db

CLIENT = Client()
NEWS_DETAIL = lf('news_detail')
NEWS_HOME = lf('news_home')
NEWS_LOGIN = lf('login')
NEWS_LOGOUT = lf('logout')
NEWS_SIGNUP = lf('signup')
AUTH_READER = lf('auth_reader')
AUTH_AUTHOR = lf('auth_author')
COMMENT_EDIT = lf('comment_edit')
COMMENT_DELETE = lf('comment_delete')
REDIRECT_URL_EDIT_COMMENT = lf('redirect_url_edit_comment')
REDIRECT_URL_DELETE_COMMENT = lf('redirect_url_delete_comment')


@pytest.mark.parametrize(
    'url, user, expected_status',
    (
        (NEWS_LOGIN, CLIENT, HTTPStatus.OK),
        (NEWS_LOGOUT, CLIENT, HTTPStatus.OK),
        (NEWS_SIGNUP, CLIENT, HTTPStatus.OK),
        (NEWS_DETAIL, CLIENT, HTTPStatus.OK),
        (NEWS_HOME, CLIENT, HTTPStatus.OK),
        (COMMENT_EDIT, AUTH_READER, HTTPStatus.NOT_FOUND),
        (COMMENT_DELETE, AUTH_AUTHOR, HTTPStatus.OK),
    ),

)
def test_pages_availability_for_users(url, user, expected_status):
    assert user.get(url).status_code == expected_status


@pytest.mark.parametrize(
    'url, user, expected_redirect',
    (
        (COMMENT_EDIT, CLIENT, REDIRECT_URL_EDIT_COMMENT),
        (COMMENT_DELETE, CLIENT, REDIRECT_URL_DELETE_COMMENT),
    ),

)
def test_redirects(url, user, expected_redirect):
    assertRedirects(user.get(url), expected_redirect)

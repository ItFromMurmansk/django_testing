from http import HTTPStatus

import pytest
from django.test.client import Client
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db

CLIENT = Client()
NEWS_DETAIL = pytest.lazy_fixture('news_detail')
NEWS_HOME = pytest.lazy_fixture('news_home')
NEWS_LOGIN = pytest.lazy_fixture('login')
NEWS_LOGOUT = pytest.lazy_fixture('logout')
NEWS_SIGNUP = pytest.lazy_fixture('signup')
AUTH_READER = pytest.lazy_fixture('auth_reader')
AUTH_AUTHOR = pytest.lazy_fixture('auth_author')
COMMENT_EDIT = pytest.lazy_fixture('comment_edit')
COMMENT_DELETE = pytest.lazy_fixture('comment_delete')
REDIRECT_URL_EDIT_COMMENT = pytest.lazy_fixture('redirect_url_edit_comment')
REDIRECT_URL_DELETE_COMMENT = (pytest
                               .lazy_fixture('redirect_url_delete_comment'))


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

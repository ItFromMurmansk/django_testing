from http import HTTPStatus

from .lib import (
    TestBasicClass,
    NOTES_ADD,
    NOTES_DELETE,
    NOTES_DETAIL,
    NOTES_EDIT,
    NOTES_HOME,
    NOTES_LIST,
    NOTES_SUCCESS,
    USERS_LOGIN,
    USERS_LOGOUT,
    USERS_SIGNUP,
    REDIRECT
)


class TestRoutes(TestBasicClass):

    def test_availability_for_pages(self):
        urls = (
            (NOTES_DELETE, self.auth_author, HTTPStatus.OK),
            (NOTES_DELETE, self.auth_reader, HTTPStatus.NOT_FOUND),
            (NOTES_EDIT, self.auth_author, HTTPStatus.OK),
            (NOTES_EDIT, self.auth_reader, HTTPStatus.NOT_FOUND),
            (NOTES_DELETE, self.auth_author, HTTPStatus.OK),
            (NOTES_DELETE, self.auth_reader, HTTPStatus.NOT_FOUND),
            (NOTES_LIST, self.auth_author, HTTPStatus.OK),
            (NOTES_ADD, self.auth_author, HTTPStatus.OK),
            (NOTES_SUCCESS, self.auth_author, HTTPStatus.OK),
            (NOTES_HOME, self.client, HTTPStatus.OK),
            (USERS_LOGIN, self.client, HTTPStatus.OK),
            (USERS_LOGOUT, self.client, HTTPStatus.OK),
            (USERS_SIGNUP, self.client, HTTPStatus.OK),
        )
        for url, user, status in urls:
            with self.subTest(url=url, user=user, status=status):
                self.assertEqual(user.get(url).status_code, status)

    def test_redirect_for_anonymous_client(self):
        urls = (NOTES_LIST,
                NOTES_EDIT,
                NOTES_DELETE,
                NOTES_DETAIL,
                NOTES_SUCCESS,
                NOTES_ADD
                )
        for url in urls:
            with self.subTest(url=url):
                self.assertRedirects(self.client.get(url), REDIRECT + url)

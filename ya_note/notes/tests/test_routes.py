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

    def test_pages_availability_anonymous(self):
        urls = (
            (NOTES_HOME),
            (USERS_LOGIN),
            (USERS_LOGOUT),
            (USERS_SIGNUP),
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_authorized(self):
        urls = (
            (NOTES_LIST),
            (NOTES_SUCCESS),
            (NOTES_ADD),
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.auth_author.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_note_edit_and_delete(self):
        self.client.logout()
        users_statuses = (
            (self.auth_reader, HTTPStatus.NOT_FOUND),
            (self.auth_author, HTTPStatus.OK),

        )
        for user, status in users_statuses:
            urls = (
                (NOTES_EDIT),
                (NOTES_DELETE),
                (NOTES_DETAIL),
            )
            for url in urls:
                with self.subTest(user=user, url=url):
                    response = user.get(url)
                    self.assertEqual(response.status_code, status)

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

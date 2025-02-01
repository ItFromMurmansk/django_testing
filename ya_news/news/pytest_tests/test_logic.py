from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db

FORM_DATA = {'text': 'Текст'}


def test_anonymous_user_cant_create_comment(
        client,
        news_detail,
        login,
):
    before_comment_count = Comment.objects.count()
    response = client.post(news_detail, data=FORM_DATA)
    after_comment_count = Comment.objects.count()
    assertRedirects(response, f'{login}?next={news_detail}')
    assert before_comment_count == after_comment_count


def test_auth_user_can_create_comment(
        auth_author,
        author,
        news_detail,
        news
):
    Comment.objects.all().delete()
    before_comment_count = Comment.objects.count()
    response = auth_author.post(news_detail, data=FORM_DATA)
    after_comment_count = Comment.objects.count()
    assertRedirects(response, news_detail + '#comments')
    assert after_comment_count - 1 == before_comment_count
    new_comment = Comment.objects.latest('id')
    assert new_comment.text == FORM_DATA['text']
    assert new_comment.news == news
    assert new_comment.author == author


def test_user_cant_use_bad_words(auth_reader, news_detail):
    bad_word_text = {
        'text': BAD_WORDS[0]
    }
    before_comment_count = Comment.objects.count()
    response = auth_reader.post(news_detail, data=bad_word_text)
    after_comment_count = Comment.objects.count()
    assert before_comment_count == after_comment_count
    assertFormError(response, form='form', field='text', errors=WARNING)


def test_author_can_edit_comment(
        auth_author,
        comment,
        comment_edit,
        news_detail,
        author,
        news
):
    response = auth_author.post(comment_edit, data=FORM_DATA)
    assertRedirects(response, news_detail + '#comments')
    comment_text = Comment.objects.get(id=comment.id)
    assert comment.text == FORM_DATA['text']
    assert comment.author == comment_text.author
    assert comment.news == comment_text.news


def test_author_can_delete_comment(
        auth_author,
        comment,
        comment_delete,
        news_detail
):
    count_before_delete = Comment.objects.count()
    response = auth_author.post(comment_delete)
    assertRedirects(response, news_detail + '#comments')
    count_after_delete = Comment.objects.count()
    assert count_before_delete - 1 == count_after_delete
    assert not Comment.objects.filter(pk=comment.id).exists()


def test_other_cant_edit_comment(
        auth_reader,
        comment,
        comment_edit,
):
    response = auth_reader.post(comment_edit, data=FORM_DATA)
    comment_text = Comment.objects.get(id=comment.id)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment.text == comment_text.text
    assert comment.news == comment_text.news
    assert comment.author == comment_text.author


def test_other_cant_delete_comment(
        auth_reader,
        comment,
        comment_delete
):
    response = auth_reader.post(comment_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.filter(pk=comment.id).exists()

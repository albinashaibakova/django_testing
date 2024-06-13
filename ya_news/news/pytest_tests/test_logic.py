import pytest

from http import HTTPStatus

from pytest_django.asserts import assertRedirects, assertFormError

from django.urls import reverse

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client,
                                            id_for_args_news,
                                            form_data):
    url = reverse('news:detail', args=id_for_args_news)
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_user_can_create_note(author_client, id_for_args_news,
                              form_data, news, author):
    url = reverse('news:detail', args=id_for_args_news)
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author
    assert new_comment.news == news


def test_user_cant_use_bad_words(author_client, id_for_args_news):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    url = reverse('news:detail', args=id_for_args_news)
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_edit_comment(author_client, form_data,
                                 comment, id_for_args_comment,
                                 id_for_args_news, new_text):
    url = reverse('news:edit', args=id_for_args_comment)
    url_comments = reverse('news:detail', args=id_for_args_news)
    form_data['text'] = new_text
    response = author_client.post(url, form_data)
    assertRedirects(response,
                    f'{url_comments}#comments')
    comment.refresh_from_db()
    assert comment.text == new_text


def test_user_cant_edit_comment_of_another_user(not_author_client,
                                                form_data, comment,
                                                id_for_args_comment, new_text):
    url = reverse('news:edit', args=id_for_args_comment)
    form_data['text'] = new_text
    response = not_author_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == comment.text


def test_author_can_delete_comment(author_client,
                                   id_for_args_comment, id_for_args_news):
    url = reverse('news:delete', args=id_for_args_comment)
    url_comments = reverse('news:detail', args=id_for_args_news)
    response = author_client.post(url)
    assertRedirects(response, f'{url_comments}#comments')
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(not_author_client,
                                                  id_for_args_comment):
    url = reverse('news:delete', args=id_for_args_comment)
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.utils.functional import cached_property

from cadizm.headspace.models import Book


class BaseResponse(JsonResponse):
    def __init__(self, *args, **kwargs):
        self.status_code = kwargs.get('status', 200)
        self.reason = kwargs.get('reason', None)
        super(BaseResponse, self).__init__(self.response(), *args, **kwargs)

    def response(self):
        response = dict(meta=self.meta())
        if self.result is not None:
            response.update(result=self.result)

        return response

    @cached_property
    def result(self):
        raise NotImplementedError()

    def meta(self):
        meta = dict(status=self.status_code)
        if self.reason:
            meta.update(reason=self.reason)

        return meta


class ErrorResponse(BaseResponse):
    def __init__(self, *args, **kwargs):
        kwargs.update(status=400)
        super(ErrorResponse, self).__init__(*args, **kwargs)

    @cached_property
    def result(self):
        pass


class CreateUserResponse(BaseResponse):
    def __init__(self, user, book_ids=None, invalid_book_ids=None, *args, **kwargs):
        kwargs.update(status=201)
        self.user = user
        self.book_ids, self.invalid_book_ids = self.validate_book_ids(book_ids)
        super(CreateUserResponse, self).__init__(*args, **kwargs)

    @cached_property
    def result(self):
        result = dict(username=self.user.username)
        if self.book_ids:
            result.update(book_ids=self.book_ids)
        if self.invalid_book_ids:
            result.update(invalid_book_ids=self.invalid_book_ids)

        return result

    def validate_book_ids(self, book_ids):
        if not book_ids:
            return [], []

        valid_book_ids = set([b.id for b in Book.objects.filter(id__in=book_ids)])
        invalid_book_ids = set(book_ids) - valid_book_ids

        return list(valid_book_ids), list(invalid_book_ids)


class CreateBookResponse(BaseResponse):
    def __init__(self, book, *args, **kwargs):
        kwargs.update(status=201)
        self.book = book
        super(CreateBookResponse, self).__init__(*args, **kwargs)

    @cached_property
    def result(self):
        return dict(title=self.book.title, author=self.book.author, book_id=self.book.id)


class AddBookResponse(BaseResponse):
    def __init__(self, library_book, *args, **kwargs):
        kwargs.update(status=200),
        self.library_book = library_book
        super(AddBookResponse, self).__init__(*args, **kwargs)

    @cached_property
    def result(self):
        pass


class DeleteBookResponse(BaseResponse):
    def __init__(self, (n, d), *args, **kwargs):
        kwargs.update(status=200)
        super(DeleteBookResponse, self).__init__(*args, **kwargs)

    @cached_property
    def result(self):
        pass


class MarkBookReadResponse(BaseResponse):
    def __init__(self, *args, **kwargs):
        kwargs.update(status=200)
        super(MarkBookReadResponse, self).__init__(*args, **kwargs)

    @cached_property
    def result(self):
        pass


class MarkBookUnreadResponse(BaseResponse):
    def __init__(self, *args, **kwargs):
        kwargs.update(status=200)
        super(MarkBookUnreadResponse, self).__init__(*args, **kwargs)

    @cached_property
    def result(self):
        pass


class ListUsersResponse(BaseResponse):
    def __init__(self, users, *args, **kwargs):
        kwargs.update(status=200)
        self.users = users
        super(ListUsersResponse, self).__init__(*args, **kwargs)

    @cached_property
    def result(self):
        result = dict(users=[])
        for user in self.users:
            result['users'].append(dict(username=user.username))

        return result


class ListBooksResponse(BaseResponse):
    def __init__(self, books, *args, **kwargs):
        kwargs.update(status=200)
        self.books = books
        super(ListBooksResponse, self).__init__(*args, **kwargs)

    @cached_property
    def result(self):
        result = dict(books=[])
        for book in self.books:
            result['books'].append(dict(book_id=book.id, title=book.title, author=book.author))

        return result


class ListLibraryResponse(BaseResponse):
    def __init__(self, library_books, *args, **kwargs):
        kwargs.update(status=200)
        self.library_books = library_books
        super(ListLibraryResponse, self).__init__(*args, **kwargs)

    @cached_property
    def result(self):
        result = dict(books=[])
        for library_book in self.library_books:
            book = library_book.book
            result['books'].append(dict(book_id=book.id, title=book.title, author=book.author, read=library_book.read))

        return result

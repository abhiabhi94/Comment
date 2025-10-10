django-comments-dab
===================

.. image:: https://img.shields.io/pypi/pyversions/django-comments-dab.svg
    :target: https://pypi.python.org/pypi/django-comments-dab/
    :alt: python

.. image:: https://img.shields.io/pypi/djversions/django-comments-dab.svg
    :target: https://pypi.python.org/pypi/django-comments-dab/
    :alt: django

.. image:: https://img.shields.io/github/license/abhiabhi94/Comment?color=gr
    :target: https://github.com/abhiabhi94/Comment/blob/develop/LICENSE
    :alt: license

.. image:: https://readthedocs.org/projects/django-comment-dab/badge/?version=latest
    :target: https://django-comment-dab.readthedocs.io/?badge=latest
    :alt: docs

.. image:: https://github.com/abhiabhi94/Comment/actions/workflows/tests.yml/badge.svg?branch=develop
    :target: https://github.com/abhiabhi94/Comment/actions
    :alt: Test

.. image:: https://codecov.io/gh/abhiabhi94/Comment/branch/develop/graph/badge.svg?token=JBorE9i0De
    :target: https://codecov.io/gh/abhiabhi94/Comment
    :alt: Coverage


.. image:: ../_static/img/comment.gif

Introduction
============

**dab stands for Django-Ajax-Bootstrap**
PS: Ajax and JQuery are not used anymore since v2.0.0 Vanilla JS and fetch API is used instead.

``django-comments-dab`` is a commenting application for Django-powered websites.

It allows you to integrate commenting functionality with any model you have e.g. blogs, pictures, video etc…

*List of actions that can be performed:*

    1. Post a new comment. (v2.0.0 authenticated and anonymous users)

    2. Reply to an existing comment. (v2.0.0 authenticated and anonymous users)

    3. Edit a comment. (authenticated user `comment owner`)

    4. Delete a comment. (authenticated user `comment owner` and admins)

    5. React to a comment. (authenticated users) Available reactions are LIKE and DISLIKE  # open PR if you would like to have more reactions

    6. Report (flag) a comment. (authenticated users)

    7. Delete flagged comment. (admins and moderators)

    8. Resolve or reject flag. This is used to revoke the flagged comment state (admins and moderators)

    9. Follow and unfollow thread. (authenticated users)

    10. Block users/emails (v2.7.0 admins and moderators)

- All actions are done by Fetch API since V2.0.0

- Bootstrap 4.1.1 is used in comment templates for responsive design.

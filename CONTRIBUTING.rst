Contributing
=============

Django Comments Dab is developed and maintained by developers in an Open Source manner.
Any support is welcome. You could help by writing documentation, pull-requests, report issues and/or translations.

Starting points
^^^^^^^^^^^^^^^^

An issue with a `good first`_ label might be a good place to start with.

You can also try to take up an issue tagged with an `upcoming release`_.

.. _`good first`: https://github.com/abhiabhi94/Comment/issues?q=is%3Aopen+is%3Aissue+label%3A"good+first+issue"
.. _`upcoming release`: https://github.com/abhiabhi94/Comment/milestones


Development
^^^^^^^^^^^

To start development on this project, fork_ this repository and follow the guidelines given below.

.. _fork: https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/fork-a-repo

.. code:: bash

    # clone the forked repository
    $ git clone YOUR_FORKED_REPO_URL

    # create a virtual environment
    $ python3 -m venv local_env
    # activate the virtual environment
    $ . local_env/bin/activate
    # install dependencies
    (local_env) $ pip install -e . -r test/example/requirements.txt

    (local_env) $ export DEBUG="True"
    # migrate the changes to database
    (local_env) $ python manage.py migrate
    # prepare initial data
    (local_env) $ python manage.py create_initial_data
    # start the development server
    (local_env) $ python manage.py runserver

Or run with docker

.. code:: bash

    $ git clone YOUR_FORKED_REPO_URL
    $ cd Comment
    $ docker-compose up


Login with:

    username: ``test``

    password: ``test``

Testing
^^^^^^^

To run tests against a particular ``python`` and ``django`` version installed inside your virtual environment, you may use:

.. code:: bash

    (local_env) $ python manage.py compilemessages -l test
    (local_env) $ python manage.py test --settings=test.settings.test


To run tests against all supported ``python`` and ``django`` versions, you may run:

.. code:: bash

    # install dependency
    (local_env) $ pip install tox
    # run tests
    (local_env) $ tox


Translations
^^^^^^^^^^^^

To add translations in your native language, please take a look at the `guidelines for translators`_.

.. _`guidelines for translators`: https://comment.readthedocs.io/en/latest/i18n.html#adding-support-for-translation

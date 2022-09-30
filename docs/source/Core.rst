==================
Core - MetabaseApi
==================

The MetabaseApi class is the core component of the API wrapper and you'll need to get it started before you do anything else.

**************
Authentication
**************

There are 3 authentication options currently supported:

Option 1 - Username and password dictionary (recommended)
=========================================================

This option involves passing a username and password in a dictionary to authenticate.

.. literalinclude:: ./examples/Core/auth_with_password.py
    :language: python
    :linenos:
    :emphasize-lines: 4-5

Option 2 - Token file
=====================

This option is best when you've previously authenticated with username and password and wish to reuse the same token. You can pass the path as a string or a pathlib.Path object.

.. literalinclude:: ./examples/Core/auth_with_token_file.py
    :language: python
    :linenos:
    :emphasize-lines: 4-5

Contents of metabase.token:

.. literalinclude:: ./examples/metabase_token

Option 3 - Token dictionary
===========================

This option involves getting the token string from your Metabase cookie so is much more involved than the other two.

.. literalinclude:: ./examples/Core/auth_with_token_dict.py
    :language: python
    :linenos:
    :emphasize-lines: 4-5

**************
Caching Tokens
**************

If you would like to cache your token for future runs to speed things up, simply set ``cache_token`` option to ``True``. This option works regardless of which authentication method was used. The token will be saved to ``token_path``.

.. literalinclude:: ./examples/Core/caching_tokens.py
    :language: python
    :linenos:
    :emphasize-lines: 4-7

********************
Other Public Methods
********************


Testing for successful authentication
=====================================

Authentication will be tested during initialization but if you would like to test after that, you can call the ``test_for_auth`` method. This will make a test call to the Metabase API and return ``True`` if it completed without issue or ``False`` otherwise.

.. autofunction:: metabase_tools.MetabaseApi.test_for_auth

Making generic requests
=======================

To make custom calls to the Metabase API, you can use the ``generic_request`` method. In general, it's better to use class-specific methods to call the methods you need but this can be used for unsupported endpoints while still utilizing the cached authentication of the wrapper.

.. autofunction:: metabase_tools.MetabaseApi.generic_request

For convenience, there are also methods to utilize for ``get``, ``delete``, ``post``, and ``put`` HTTP verbs:

.. autofunction:: metabase_tools.MetabaseApi.get

.. autofunction:: metabase_tools.MetabaseApi.delete

.. autofunction:: metabase_tools.MetabaseApi.post

.. autofunction:: metabase_tools.MetabaseApi.put

Custom Session objects
======================

If you need to make use of a proxy or other feature supported by the requests module's Session class, you can pass it in to the adapter on creation.

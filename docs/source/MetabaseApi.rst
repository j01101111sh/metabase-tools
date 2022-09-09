===========
MetabaseApi
===========

The MetabaseApi class is the core component of the API wrapper and you'll need to get it started before you do anything else.

**************
Authentication
**************

There are 3 authentication options currently supported:

Option 1 - Username and password dictionary (recommended)
=========================================================

This option involves passing a username and password in a dictionary to authenticate.

.. literalinclude:: ./examples/MetabaseApi/auth_with_password.py
    :language: python

Option 2 - Token file
=====================

This option is best when you've previously authenticated with username and password and wish to reuse the same token. You can pass the path as a string or a pathlib.Path object.

.. literalinclude:: ./examples/MetabaseApi/auth_with_token_file.py
    :language: python

Contents of metabase.token:

.. literalinclude:: ./examples/metabase.token

Option 3 - Token dictionary
===========================

This option involves getting the token string from your Metabase cookie so is much more involved than the other two.

.. literalinclude:: ./examples/MetabaseApi/auth_with_token_dict.py
    :language: python

**************
Caching tokens
**************

If you would like to cache your token for future runs to speed things up, simply set ``cache_token`` option to ``True``. This option works regardless of which authentication method was used. The token will be saved to ``token_path``.

.. literalinclude:: ./examples/MetabaseApi/caching_tokens.py
    :language: python

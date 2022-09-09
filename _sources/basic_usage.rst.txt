===========
Basic Usage
===========

************
Installation
************

To use metabase-tools, first install it using pip or poetry:

.. code-block:: console

   (.venv) $ pip install metabase-tools

**OR**

.. code-block:: console

   (.venv) $ poetry add metabase-tools

***********
General Use
***********

The most basic use of the wrapper is to call a Metabase API endpoint so you do not need to manage authentication yourself. 

There are two kinds of endpoints currently supported:
- Endpoints that either create new objects or deal with groups (i.e. lists) of existing objects (e.g. getting a list)
- Endpoints acting on an existing object (e.g. updates)

These two kinds of endpoints are handled separately in the wrapper to make calling their methods more convenient. For details on available methods, you will need to see the relevant page for each object type.

Type 1 - New or grouped object methods
======================================

The following methods are supported for all current objects:
- create
- get
- search

You will need to access these methods through the appropriate member of MetabaseApi after initialization, as seen here:

.. literalinclude:: ./examples/basic_usage/get_cards.py
    :language: python

Type 2 - Single, existing object methods
========================================

If a method acts on a single, existing object, you need to get an instance of that object first and call the method from that object, as seen here:

.. literalinclude:: ./examples/basic_usage/archive_card.py
    :language: python

If you need to apply an action to many objects at once, you can loop through them in a list comprehension:

.. literalinclude:: ./examples/basic_usage/archive_many_cards.py
    :language: python
    :emphasize-lines: 9
    :linenos:

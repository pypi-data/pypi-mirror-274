DatabaseQuery
=============

**Parameter specifications**:

Each parameter can only take specific strings (e.g. spelling of certain country names) that are defined in the database.
Leaving the filters empty will return all data. You can find these exact strings in following files:

.. toctree::
   :maxdepth: 1

   receiver_region
   receiver_country
   receiver_category
   initiator_country
   date_type
   flag_type

.. automodule:: eurepoc.database_query
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __dict__,__weakref__,__module__,__init__,_query_database

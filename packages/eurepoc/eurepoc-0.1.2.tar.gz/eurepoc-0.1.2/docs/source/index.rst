.. eurepoc documentation master file, created by
   sphinx-quickstart on Fri May 17 15:41:39 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

EuRepoC Package Documentation
===================================
The EuRepoC package is a wrapper around the main EuRepoC Strapi API. It is designed to streamline
data queries through a set of filters and to preprocess, unnest and clean the Strapi output. The
`IncidentDataFrames` class automatically converts the data into multiple pandas dataframes (dfs) for easier
manipulation and analysis. These dfs can be easily joined using the `incidents_id` column.

Refer to the main EuRepoC website (https://www.eurepoc.eu/) for more information about the data collection
methodology. The EuRepoC Codebook provides detailed information about the substantive meaning of each of the
variables in the data here: https://eurepoc.eu/wp-content/uploads/2023/07/EuRepoC_Codebook_1_2.pdf.

Quickstart
==========

Install the package:

.. code-block:: bash

    $ pip install eurepoc

Example usage:

.. code-block:: python

    import eurepoc

    TOKEN = eurepoc.read_token()

    query_db = eurepoc.DatabaseQuery(
         TOKEN,
         receiver_region="EU",
         receiver_category="Critical infrastructure",
         initiator_country="Russia"
      )

    data = query_db.get_data()

    incident_df = eurepoc.IncidentDataFrames(data)
    receivers = incident_df.receivers()
    attributions = incident_df.attributions()
    initiators = incident_df.initiators()

Contents
========

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   read_token
   DatabaseQuery
   IncidentDataFrames

Indices and tables
==================

* :ref:`search`

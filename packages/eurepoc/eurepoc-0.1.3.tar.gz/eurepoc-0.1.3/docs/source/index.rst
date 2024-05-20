.. eurepoc documentation master file, created by
   sphinx-quickstart on Fri May 17 15:41:39 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

EuRepoC Package Documentation
===================================
The EuRepoC package is a wrapper around the main EuRepoC Strapi API. It is designed to streamline
data queries through a set of filters and to preprocess, unnest and clean the Strapi output. The
`IncidentDataFrameGenerator` class automatically converts the data into multiple pandas dataframes (dfs) for easier
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

    query = eurepoc.DatabaseQuery(
       TOKEN,
       receiver_region="EU",
       receiver_category="Critical infrastructure",
       initiator_country="Russia"
    )

    data = query.execute_query()

    df_generator = eurepoc.IncidentDataFrameGenerator(data)

    main_df = df_generator.get_main_data()
    receivers_df = df_generator.get_receivers()
    attributions_df = df_generator.get_attributions()
    initiators_df = df_generator.get_initiators()

Contents
========

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   read_token
   DatabaseQuery
   IncidentDataFrameGenerator

Indices and tables
==================

* :ref:`search`

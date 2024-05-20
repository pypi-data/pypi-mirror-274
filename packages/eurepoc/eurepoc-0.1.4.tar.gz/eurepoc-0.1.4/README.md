# eurepoc

🚀 The EuRepoC package is a wrapper around the main EuRepoC Strapi API. It is designed to streamline data queries through a set of filters and to preprocess, unnest and clean the Strapi output. The IncidentDataFrames class automatically converts the data into multiple pandas dataframes (dfs) for easier manipulation and analysis. These dfs can be easily joined using the incidents_id column.

🔎 Refer to the main [EuRepoC website](https://www.eurepoc.eu/) for more information about the data collection methodology. 
The EuRepoC Codebook provides detailed information about the substantive meaning of each of the variables in the data [here](https://eurepoc.eu/methodology/).

📖 **The package documentation is available [here](https://eurepoc.readthedocs.io/en/latest/)**

## Installation

```bash
pip install eurepoc
```

## Quickstart

```python
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
```
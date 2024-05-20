from eurepoc.data_cleaning_utils import get_clean_data
from eurepoc.data_query_utils import query_database


class DatabaseQuery:
    """
        A class used for querying and processing the data from the EuRepoC Strapi API using specified filters.

        Parameters:
            token (str): Authentication token for the EuRepoC database.
            receiver_region (str, optional): Default is None.
            receiver_country (str, optional): Default is None.
            receiver_category (str, optional): Default is None.
            initiator_country (str, optional): Default is None.
            date_type (str, optional): Refers to the type of date to filter by. This can be either: 'start_date', referring to the start date of the incident; or 'createdAt', referring to the date the incident was added to the database. Default is None.
            start_date (str, optional): The start date for filtering data (YYYY-MM-DD format). Default is None.
            end_date (str, optional): The end date for filtering data (YYYY-MM-DD format). Default is None.
            flag_type (str, optional): Default is None.
            flag_status (str, optional): Default is None.

        Raises:
            ValueError: If no token is provided.
        """
    def __init__(
            self,
            token: str,
            receiver_region: str = None,
            receiver_country: str = None,
            receiver_category: str = None,
            initiator_country: str = None,
            date_type: str = None,
            start_date: str = None,
            end_date: str = None,
            flag_type: str = None,
            flag_status: str = None
    ):
        if not token:
            raise ValueError("A valid token must be provided.")

        self.token = token
        self.flag_type = flag_type
        self.flag_status = flag_status
        self.receiver_region = receiver_region
        self.receiver_country = receiver_country
        self.receiver_category = receiver_category
        self.initiator_country = initiator_country
        self.date_type = date_type
        self.range_start_date = start_date
        self.range_end_date = end_date

    def execute_query(self):
        """
        Fetches and cleans data from the EuRepoC database.

        Returns:
            (list): A list of dictionaries, one per incident containing all cleaned and unnested variables from the database.
        """
        try:
            raw_data = self._query_database()
            if raw_data is not None:
                return get_clean_data(raw_data, receiver_region=self.receiver_region)
            return None
        except Exception as e:
            print(f"Error processing data: {e}")
            return None

    def _query_database(self):
        """Performs a database query using the instance's configuration."""
        return query_database(
            token=self.token,
            flag_type=self.flag_type, flag_status=self.flag_status,
            receiver_region=self.receiver_region, receiver_country=self.receiver_country,
            date_type=self.date_type, range_start_date=self.range_start_date, range_end_date=self.range_end_date,
            receiver_category=self.receiver_category, initiator_country=self.initiator_country
        )

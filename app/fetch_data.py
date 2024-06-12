import logging
import pandas as pd
import io


def fetch_data(data_url: str, fetcher_func) -> pd.DataFrame:
    """
    Fetch data using the provided fetching function and return a DataFrame.

    Args:
        data_url (str): The URL from which to fetch data.
        fetcher_func (callable): A function that takes a URL and returns a BytesIO stream.

    Returns:
        pd.DataFrame: The DataFrame loaded from the data URL, or None if an error occurs.

    Raises:
        Exception: Propagates exceptions that are not handled internally, indicating an unexpected error.
    """
    try:
        logging.info(f"Attempting to fetch data from data URL")
        data_stream = fetcher_func(data_url)
        
        if data_stream and isinstance(data_stream, io.BytesIO):
            logging.debug("Data stream successfully retrieved, loading into DataFrame.")
            df = pd.read_csv(data_stream)
            return df
        else:
            logging.warning(f"No data stream returned from fetcher function for URL: {data_url}")
            return None
    except pd.errors.EmptyDataError as e:
        logging.error(f"No data to parse from URL: {data_url} - {e}")
    except pd.errors.ParserError as e:
        logging.error(f"Error parsing data from URL: {data_url} - {e}")
    except Exception as e:
        logging.exception(f"Unexpected error fetching data from URL: {data_url}")
        raise  # Optionally re-raise the exception if you want to handle it further up the call stack
    return None

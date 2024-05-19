def read_token(text_file='API_token.txt'):
    """
        Retrieves the API token from a specified text file.

        Parameters:
            text_file (str): The path to the text file containing the API token. Defaults to 'API_token.txt'.

        Returns:
            str: The API token as a string.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the token file is empty.
            Exception: For other issues that prevent reading the token, with a message indicating the error.
        """
    try:
        with open(text_file, 'r') as f:
            token = f.readline().strip()
            if not token:
                raise ValueError("Token file is empty")
            return token
    except FileNotFoundError:
        raise FileNotFoundError("Token file not found")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

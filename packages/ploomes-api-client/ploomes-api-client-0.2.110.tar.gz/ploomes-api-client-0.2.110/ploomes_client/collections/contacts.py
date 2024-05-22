import pytz
import json
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from ploomes_client.core.ploomes_client import PloomesClient
from ploomes_client.core.utils import get_file_url
from datetime import datetime


class Contacts:
    def __init__(self, client: PloomesClient) -> None:
        self.client = client
        self.path = "/Contacts"

    def get_contacts(
        self,
        filter_=None,
        expand=None,
        top=None,
        inlinecount=None,
        orderby=None,
        select=None,
        skip=None,
    ):
        """
        Creates a new contact using the provided payload and filters.

        Args:
            payload (dict): The data for the contact to be created.
            filter_ (str, optional): OData filter string.
            expand (str, optional): Expand related entities.
            top (int, optional): Maximum number of results to return.
            inlinecount (str, optional): Option for inline count.
            orderby (str, optional): Order by clause.
            select (str, optional): Select specific properties.
            skip (int, optional): Number of results to skip.

        Returns:
            Response: The response object containing the result of the POST request.
        """
        filters = {
            "$filter": filter_,
            "$inlinecount": inlinecount,
            "$orderby": orderby,
            "$select": select,
            "$skip": skip,
            "$top": top,
            "$expand": expand,
        }
        return self.client.request(
            "GET",
            self.path,
            filters={k: v for k, v in filters.items() if v is not None},
        )

    def get_contacts_products(
        self,
        filter_=None,
        expand=None,
        top=None,
        inlinecount=None,
        orderby=None,
        select=None,
        skip=None,
    ):
        """
        Creates a new contact using the provided payload and filters.

        Args:
            payload (dict): The data for the contact to be created.
            filter_ (str, optional): OData filter string.
            expand (str, optional): Expand related entities.
            top (int, optional): Maximum number of results to return.
            inlinecount (str, optional): Option for inline count.
            orderby (str, optional): Order by clause.
            select (str, optional): Select specific properties.
            skip (int, optional): Number of results to skip.

        Returns:
            Response: The response object containing the result of the POST request.
        """
        filters = {
            "$filter": filter_,
            "$inlinecount": inlinecount,
            "$orderby": orderby,
            "$select": select,
            "$skip": skip,
            "$top": top,
            "$expand": expand,
        }
        return self.client.request(
            "GET",
            self.path + "@Products",
            filters={k: v for k, v in filters.items() if v is not None},
        )

    def get_contacts_origins(
        self,
        filter_=None,
        expand=None,
        top=None,
        inlinecount=None,
        orderby=None,
        select=None,
        skip=None,
    ):
        """
        Creates a new contact using the provided payload and filters.

        Args:
            payload (dict): The data for the contact to be created.
            filter_ (str, optional): OData filter string.
            expand (str, optional): Expand related entities.
            top (int, optional): Maximum number of results to return.
            inlinecount (str, optional): Option for inline count.
            orderby (str, optional): Order by clause.
            select (str, optional): Select specific properties.
            skip (int, optional): Number of results to skip.

        Returns:
            Response: The response object containing the result of the POST request.
        """
        filters = {
            "$filter": filter_,
            "$inlinecount": inlinecount,
            "$orderby": orderby,
            "$select": select,
            "$skip": skip,
            "$top": top,
            "$expand": expand,
        }
        return self.client.request(
            "GET",
            self.path + "@Origins",
            filters={k: v for k, v in filters.items() if v is not None},
        )

    def post_contact(
        self,
        payload,
        filter_=None,
        expand=None,
        top=None,
        inlinecount=None,
        orderby=None,
        select=None,
        skip=None,
    ):
        filters = {
            "$filter": filter_,
            "$inlinecount": inlinecount,
            "$orderby": orderby,
            "$select": select,
            "$skip": skip,
            "$top": top,
            "$expand": expand,
        }
        payload_json = json.dumps(payload)
        return self.client.request(
            "POST",
            self.path,
            filters={k: v for k, v in filters.items() if v is not None},
            payload=payload_json,
        )

    def post_contact_products(
        self,
        payload,
        filter_=None,
        expand=None,
        top=None,
        inlinecount=None,
        orderby=None,
        select=None,
        skip=None,
    ):
        filters = {
            "$filter": filter_,
            "$inlinecount": inlinecount,
            "$orderby": orderby,
            "$select": select,
            "$skip": skip,
            "$top": top,
            "$expand": expand,
        }
        payload_json = json.dumps(payload)
        return self.client.request(
            "POST",
            self.path + "@Products",
            filters={k: v for k, v in filters.items() if v is not None},
            payload=payload_json,
        )

    def post_contact_origins(
        self,
        payload,
        filter_=None,
        expand=None,
        top=None,
        inlinecount=None,
        orderby=None,
        select=None,
        skip=None,
    ):
        filters = {
            "$filter": filter_,
            "$inlinecount": inlinecount,
            "$orderby": orderby,
            "$select": select,
            "$skip": skip,
            "$top": top,
            "$expand": expand,
        }
        payload_json = json.dumps(payload)
        return self.client.request(
            "POST",
            self.path + "@Origins",
            filters={k: v for k, v in filters.items() if v is not None},
            payload=payload_json,
        )

    def patch_contact(
        self,
        id_: int,
        payload: dict,
        filter_=None,
        expand=None,
        top=None,
        inlinecount=None,
        orderby=None,
        select=None,
        skip=None,
    ):
        """
        Updates a contact by its ID with specific fields.

        Args:
            id_ (int): The ID of the contact to be updated.
            payload (dict): Fields to be updated in the contact.
            filter_ (str, optional): OData filter string.
            inlinecount (str, optional): Option for inline count.
            orderby (str, optional): Order by clause.
            select (str, optional): Select specific properties.
            skip (int, optional): Number of results to skip.
            top (int, optional): Maximum number of results to return.
            expand (str, optional): Expand related entities.

        Returns:
            dict: The JSON response from the server.
        """
        filters = {
            "$filter": filter_,
            "$inlinecount": inlinecount,
            "$orderby": orderby,
            "$select": select,
            "$skip": skip,
            "$top": top,
            "$expand": expand,
        }
        payload_json = json.dumps(payload)
        return self.client.request(
            "PATCH",
            self.path + f"({id_})",
            filters={k: v for k, v in filters.items() if v is not None},
            payload=payload_json,
        )

    def patch_contact_products(
        self,
        id_: int,
        payload: dict,
        filter_=None,
        expand=None,
        top=None,
        inlinecount=None,
        orderby=None,
        select=None,
        skip=None,
    ):
        """
        Updates a contact by its ID with specific fields.

        Args:
            id_ (int): The ID of the contact to be updated.
            payload (dict): Fields to be updated in the contact.
            filter_ (str, optional): OData filter string.
            inlinecount (str, optional): Option for inline count.
            orderby (str, optional): Order by clause.
            select (str, optional): Select specific properties.
            skip (int, optional): Number of results to skip.
            top (int, optional): Maximum number of results to return.
            expand (str, optional): Expand related entities.

        Returns:
            dict: The JSON response from the server.
        """
        filters = {
            "$filter": filter_,
            "$inlinecount": inlinecount,
            "$orderby": orderby,
            "$select": select,
            "$skip": skip,
            "$top": top,
            "$expand": expand,
        }
        payload_json = json.dumps(payload)
        return self.client.request(
            "PATCH",
            self.path + f"@Products({id_})",
            filters={k: v for k, v in filters.items() if v is not None},
            payload=payload_json,
        )

    def delete_contact(self, id_: int):
        """
        Deletes a contact by its ID.

        Args:
            id_ (int): The ID of the contact to be deleted.

        Returns:
            dict: The JSON response from the server.
        """
        return self.client.request("DELETE", self.path + f"({id_})")

    def delete_contact_products(self, id_: int):
        """
        Deletes a contact by its ID.

        Args:
            id_ (int): The ID of the contact to be deleted.

        Returns:
            dict: The JSON response from the server.
        """
        return self.client.request("DELETE", self.path + f"@Products({id_})")

    def post_contact_avatar(self, contact_id: int, image_url: str) -> dict:
        """
        Uploads an avatar for a specific contact.
        """
        filename = get_file_url(
            image_url
        )  # Ensure this extracts the filename correctly
        files = [("file1", (filename, requests.get(image_url).content, "image/jpeg"))]

        # Make the request
        response = self.client.request(
            "POST", self.path + f"({contact_id})/UploadAvatar", files=files
        )

        return response

    def post_attachment(self, contact_id: int, file_url: str) -> dict:
        """
        Uploads an avatar for a specific contact.
        """
        response = _download_file(file_url)
        
        filename = _generate_filename(file_url, contact_id)
        files = [("file1", (filename, response.content, response.headers["Content-Type"]))]

        # Make the request
        response = self.client.request(
            "POST", self.path + f"({contact_id})/UploadFile", files=files
        )

        return response

     def _download_file(self, file_url: str, retries: int = 3, timeout: int = 10) -> requests.Response:
        """Download the file from the provided URL with retry logic and error handling."""
        for attempt in range(retries):
            try:
                response = requests.get(file_url, stream=True, timeout=timeout)
                response.raise_for_status()
                return response
            except (HTTPError, ConnectionError, Timeout) as e:
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise Exception(f"Failed to download file from {file_url} after {retries} attempts") from e
            except RequestException as e:
                raise Exception(f"An error occurred while trying to download the file from {file_url}") from e

    def _generate_filename(self, file_url: str, contact_id: int) -> str:
        """Generate a filename with metadata including contact ID, timestamp, and file type."""
        original_filename = file_url.split("/")[-1]
        file_type = original_filename.split(".")[-1] if "." in original_filename else "unknown"
        timezone = pytz.timezone('Etc/GMT+3')
        current_time = datetime.now(timezone)

        formatted_filename = (
            f"{contact_id}_{current_time.year}{current_time.month:02}{current_time.day:02}_"
            f"{current_time.hour:02}{current_time.minute:02}{current_time.second:02}_{file_type}_"
            f"{original_filename}"
        )
        return formatted_filename

    def check_duplicate_contact(self, payload: dict):
        """
        Checks for a duplicate contact by sending a POST request to the API.

        Args:
            payload (dict): Data containing the necessary parameters to check for duplicates.

        Returns:
            dict: The JSON response from the server containing the result.
        """
        payload_json = json.dumps(payload)
        return self.client.request(
            "POST", self.path + "/IsDuplicate", payload=payload_json
        )

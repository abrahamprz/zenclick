from requests import post, Response
from django.conf import settings
from io import BytesIO

class StirlingAPI():
    """
    A class that provides methods for interacting with the Stirling API.

    Attributes:
        base_url (str): The base URL of the Stirling API.
    """

    def __init__(self):
        self.base_url = settings.STIRLING_API_BASE_URL
        self.headers = {
            'accept': 'application/json',
            'X-API-KEY': f'{settings.STIRLING_API_TOKEN}'
        }
    
    def generate_pdf_from_md(self, input_file: str) -> Response:
        """
        Generates a PDF file from a Markdown file.

        Args:
            input_file (str): The path to the input Markdown file.

        Returns:
            Response: The response object from the API request.

        Raises:
            None: This method does not raise any exceptions.

        """        
        # with open(input_file, 'rb') as file:
        #     response = post(
        #     url,
        #     headers=self.headers,
        #     files={'fileInput': file}
        # )
        
        response = post(
            self.base_url + 'v1/convert/markdown/pdf',
            headers=self.headers,
            files={'fileInput': ('document.md', input_file, 'text/markdown')}
        )
        
        return response


    def merge_pdfs(self, input_files: list, sortType: str = 'orderProvided', removeCertSign: bool = True) -> Response:
        """
        Merges multiple PDF files into a single PDF file.

        Args:
            input_files (list): array($binary) The PDF files to merge.
            sortType (str): The type of sorting to apply to the merged PDFs. Possible values 'orderProvided', 'byFileName', 'byDateModified', 'byDateCreated' and 'byPDFTitle'.
            removeCertSign (bool): Whether to remove the certification signature from the merged PDF.

        Returns:
            Response: The response object from the API request.

        Raises:
            None: This method does not raise any exceptions.

        """
        url = self.base_url + 'v1/general/merge-pdfs'
                
        files = []
        for file in input_files:
            files.append(('fileInput', (file.split('/')[-1], open(file, 'rb'), 'application/pdf')))
        
        data = {
            'sortType': sortType,
            'removeCertSign': removeCertSign
        }
        
        response = post(
            url,
            headers=self.headers,
            files=files,
            data=data
        )
        
        # Close all opened files
        for _, file_tuple in files:
            file_tuple[1].close()
        
        return response
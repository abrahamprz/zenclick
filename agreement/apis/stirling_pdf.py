from requests import post, Response

class StirlingAPI():
    """
    A class that provides methods for interacting with the Stirling API.

    Attributes:
        base_url (str): The base URL of the Stirling API.
        
    """

    def __init__(self, base_url: str):
        self.base_url = base_url
    
    def generate_pdf_from_md(self, input_file_path: str, output_file_path: str = "") -> Response:
        """
        Generates a PDF file from a Markdown file.

        Args:
            input_file_path (str): The path to the input Markdown file.
            output_file_path (str): The path to save the output PDF file if provided.

        Returns:
            Response: The response object from the API request.

        Raises:
            None: This method does not raise any exceptions.

        """
        url = self.base_url + 'v1/convert/markdown/pdf'

        with open(input_file_path, 'rb') as file:
            response = post(
                url,
                headers={'accept': '*/*'},
                files={'fileInput': file}
            )

        # Check if the request was successful
        if response.status_code == 200:
            # Save the PDF to a file
            if output_file_path:
                with open(output_file_path, 'wb') as pdf_file:
                    pdf_file.write(response.content)
            print(f"PDF generated successfully: {output_file_path}")
        else:
            print(f"Failed to generate PDF. Status code: {response.status_code}")
            print(response.text)
        
        return response

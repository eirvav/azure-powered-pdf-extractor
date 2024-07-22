# PDF Text Extractor

This Flask application extracts text from the first two pages of uploaded PDF files using Azure Document Intelligence and the Read Model.

## Setup
1. Clone this repository.
2. Install required packages: 

`pip install flask azure-ai-formrecognizer` 

and 

`pip install azure-ai-documentintelligence==1.0.0b2`


3. Set up environment variables:
   - DOCUMENTINTELLIGENCE_ENDPOINT
     - You can use `setx DI_KEY <yourKey>` in the terminal
   - DOCUMENTINTELLIGENCE_API_KEY
     - You can use `setx DI_ENDPOINT <yourEndpoint>` in the terminal
4. Run the application: `analyze_read.py`, it should start on `http://127.0.0.1:5000`

Read the documentation further for more:
https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/how-to-guides/use-sdk-rest-api?view=doc-intel-4.0.0&tabs=windows&pivots=programming-language-python
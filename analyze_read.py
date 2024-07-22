import os
import io
from flask import Flask, request, render_template_string, send_file
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from werkzeug.utils import secure_filename

app = Flask(__name__)


def analyze_pdf(file_content):
    endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
    key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    file_stream = io.BytesIO(file_content)

    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-read",
        file_stream
    )
    result = poller.result()

    extracted_text = []
    for page_num, page in enumerate(result.pages, start=1):
        if page_num > 2:  # Only process the first two pages
            break
        extracted_text.append(f"--- Page {page_num} ---")
        for line in page.lines:
            extracted_text.append(line.content)

    return "\n".join(extracted_text)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and file.filename.lower().endswith('.pdf'):
            try:
                file_content = file.read()
                extracted_text = analyze_pdf(file_content)

                # Create a text file with the extracted content
                txt_filename = secure_filename(file.filename.rsplit('.', 1)[0] + '_extracted.txt')
                txt_path = os.path.join('temp', txt_filename)
                os.makedirs('temp', exist_ok=True)
                with open(txt_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(extracted_text)

                return render_template_string('''
                    <h2>Text Extracted Successfully</h2>
                    <p>Click the button below to download the extracted text:</p>
                    <a href="{{ url_for('download_file', filename=txt_filename) }}" download>
                        <button>Download Extracted Text</button>
                    </a>
                    <br><br>
                    <a href="/">Upload another file</a>
                ''', txt_filename=txt_filename)
            except Exception as e:
                return f"An error occurred: {str(e)}"
        else:
            return 'Invalid file type. Please upload a PDF file.'

    return '''
    <!doctype html>
    <title>Upload a PDF file</title>
    <h1>Upload a PDF file</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file accept=".pdf">
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join('temp', filename), as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
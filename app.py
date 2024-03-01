from flask import Flask, request, render_template, jsonify
import boto3
import time
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Initialize AWS credentials and clients
aws_bucket_name = os.getenv("BUCKET_NAME")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")
aws_client = os.getenv("AWS_CLIENT")

s3 = boto3.client('s3')
textract = boto3.client(aws_client, region_name=aws_region)

# Helper functions for file upload and processing
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_upload(file):
    if not file or file.filename == '':
        return None, 'No selected file or file part'
    if not allowed_file(file.filename):
        return None, 'Unsupported file type'

    file_key = 'uploads/' + file.filename
    s3.upload_fileobj(file, aws_bucket_name, file_key)
    response = textract.start_document_text_detection(
        DocumentLocation={'S3Object': {'Bucket': aws_bucket_name, 'Name': file_key}}
    )
    return response['JobId'], None

def process_textract_data(response):
    """
    Processes the data returned by Textract and extracts text and confidence scores.

    :param response: The response from Textract after processing a document.
    :return: A list of dictionaries containing the extracted text and confidence scores.
    """
    processed_data = []

    # Check if 'Blocks' is in the response
    for item in response.get('Blocks', []):
        # Process only 'LINE' block types
        if item['BlockType'] == 'LINE':
            processed_data.append({
                'text': item.get('Text', ''),
                'confidence': item.get('Confidence', 0)
            })

    return processed_data



# Flask route definitions
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('document')
    job_id, error = process_upload(file)
    if error:
        return error
    return render_template('check_status.html', job_id=job_id)

@app.route('/api/upload', methods=['POST'])
def api_upload_file():
    file = request.files.get('document')
    job_id, error = process_upload(file)
    
    # Render a template that includes JavaScript for polling
    render_template('check_status.html', job_id=job_id)
    if error:
        return jsonify({'error': error}), 400

    return jsonify({'jobId': job_id})

@app.route('/status', methods=['POST'])
def get_status():
    job_id = request.form.get('jobId')
    if not job_id:
        return jsonify({'error': 'Missing job ID'}), 400

    response = textract.get_document_text_detection(JobId=job_id)
    if response['JobStatus'] in ['SUCCEEDED', 'FAILED']:
        return jsonify({'status': response['JobStatus']})
    return jsonify({'status': 'IN_PROGRESS'})

# Improved result handling
@app.route('/result', methods=['POST'])
def get_result():
    job_id = request.form['jobId']
    if not job_id:
        return 'Missing job ID', 400

    response = textract.get_document_text_detection(JobId=job_id)
    if response['JobStatus'] == 'SUCCEEDED':
        extracted_details = process_textract_data(response)
        return render_template('result.html', extracted_details=extracted_details)
    return 'Text detection did not succeed'

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, render_template, jsonify
import boto3
import time
import os
from dotenv import load_dotenv

load_dotenv()  # This method will load the .env file
app = Flask(__name__)



aws_bucket_name = os.getenv("BUCKET_NAME")
# BUCKET_NAME = 'textra-bucket' 
# Now you can access the environment variables using os.getenv
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")
aws_client = os.getenv("AWS_CLIENT")

# Initialize the S3 and Textract clients
s3 = boto3.client('s3')
textract = boto3.client(aws_client, region_name=aws_region)

def process_upload(file):
    if not file or file.filename == '':
        return None, 'No selected file or file part'

    if allowed_file(file.filename):
        file_key = 'uploads/' + file.filename
        s3.upload_fileobj(file, aws_bucket_name, file_key)

        response = textract.start_document_text_detection(
            DocumentLocation={'S3Object': {'Bucket': aws_bucket_name, 'Name': file_key}}
        )
        return response['JobId'], None
    else:
        return None, 'Unsupported file type'

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_textract_data(response):
    """
    Processes the data returned by Textract and extracts text and confidence scores.

    :param response: The response from Textract after processing a document.
    :return: A list of dictionaries containing the extracted text and confidence scores.
    """
    processed_data = []

    # Assuming 'Blocks' contain the lines of text you're interested in
    for block in response.get('Blocks', []):
        if block['BlockType'] == 'LINE':
            text_data = {
                'text': block.get('Text', ''),
                'confidence': block.get('Confidence', 0)
            }
            processed_data.append(text_data)

    return processed_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('document')
    job_id, error = process_upload(file)

    if error:
        return error

    # Render a template that includes JavaScript for polling
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

    # Check the status of the Textract job
    response = textract.get_document_text_detection(JobId=job_id)

    if response['JobStatus'] == 'SUCCEEDED':
        # Extract relevant data from the response
        extracted_data = process_textract_data(response)
        return jsonify({'status': 'COMPLETED', 'data': extracted_data})
    elif response['JobStatus'] == 'IN_PROGRESS':
        return jsonify({'status': 'IN_PROGRESS'})
    else:
        return jsonify({'status': 'FAILED'})


@app.route('/result', methods=['POST'])
def get_result():
    if request.method == 'POST':
        job_id = request.form['jobId']

        # Poll Textract to get the job status
        response = textract.get_document_text_detection(JobId=job_id)

        # Wait for the job to complete (consider moving this to a background task or asynchronous polling instead)
        while response['JobStatus'] == 'IN_PROGRESS':
            time.sleep(5)  # Implement exponential backoff in a production environment
            response = textract.get_document_text_detection(JobId=job_id)

        # Process the response when the job is completed
        if response['JobStatus'] == 'SUCCEEDED':
            # Use the process_textract_data function to process the response
            extracted_details = process_textract_data(response)
            return render_template('result.html', extracted_details=extracted_details)
        else:
            return 'Text detection did not succeed'
    else:
        # This branch should only occur if something other than POST is used
        return "This endpoint requires a POST request."


if __name__ == '__main__':
    app.run(debug=True)


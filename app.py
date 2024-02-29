from flask import Flask, request, render_template, jsonify
import boto3
import time

app = Flask(__name__)

# Initialize the S3 and Textract clients
s3 = boto3.client('s3')
textract = boto3.client('textract', region_name='us-east-1')

BUCKET_NAME = 'textra-bucket'  # Replace with your actual S3 bucket name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'document' not in request.files:
        return 'No file part'

    file = request.files['document']

    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        file_key = 'uploads/' + file.filename
        s3.upload_fileobj(file, BUCKET_NAME, file_key)

        response = textract.start_document_text_detection(
            DocumentLocation={'S3Object': {'Bucket': BUCKET_NAME, 'Name': file_key}}
        )
        
        job_id = response['JobId']
        
        # Render a template that includes JavaScript for polling
        return render_template('check_status.html', job_id=job_id)
    else:
        return 'Unsupported file type'


@app.route('/result', methods=['GET', 'POST'])
def get_result():
    if request.method == 'POST':
        job_id = request.form['jobId']

        # Poll Textract to get the job status
        response = textract.get_document_text_detection(JobId=job_id)

        while response['JobStatus'] == 'IN_PROGRESS':
            time.sleep(5)
            response = textract.get_document_text_detection(JobId=job_id)

        if response['JobStatus'] == 'SUCCEEDED':
            details = []
            for item in response['Blocks']:
                if item['BlockType'] == 'LINE':
                    details.append({'text': item['Text'], 'confidence': item['Confidence']})

            return render_template('result.html', extracted_details=details)
        else:
            return 'Text detection did not succeed'
    else:
        # GET request: you could provide a meaningful response or redirect
        return "This endpoint requires a POST request."


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)

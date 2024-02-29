# Flask Document Processing Application with AWS Textract

This Flask application allows users to upload documents, which are then processed by AWS Textract to extract text. The extracted text is displayed to the user once processing is complete.

## Features

- File upload through a web interface.
- Integration with AWS Textract for document text extraction.
- Polling mechanism to check the status of the text extraction job.
- Display of extracted text in the web interface once processing is completed.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- Boto3
- An AWS account with access to S3 and Textract

### Installation

1. Clone the repository:
```
git clone <repository-url>
```

2. Navigate to the application directory:
```
cd <application-directory>
```

3. **Install virtualenv:**

   Before setting up the project environment, you need to install `virtualenv` if you haven't already. This tool helps create isolated Python environments. Install it globally using pip:

   ```
   pip install virtualenv
   ```

4. **Create a virtual environment:**

   Now, use `virtualenv` to create an isolated environment for your project. This environment will have its own installation directories and won't share libraries with other environments.

   ```
   virtualenv venv
   ```

   - For **Unix/Linux/macOS** to activate the virtual environment:

     ```
     source venv/bin/activate
     ```

   - For **Windows** to activate the virtual environment in Command Prompt:

     ```
     .\venv\Scripts\activate
     ```

   - For **Windows using PowerShell**:

     ```
     .\venv\Scripts\Activate.ps1
     ```


5. Install the required Python packages:
```
pip install -r requirements.txt
```

6. Set up your AWS credentials to allow your application to access AWS services:

- AWS credentials are necessary for your application to interact with AWS services and consist of an access key ID and a secret access key.
- Create a new IAM user in your AWS account dedicated to your application, granting it the necessary permissions for Amazon S3 and Amazon Textract.
- Once the IAM user is created, you will receive an access key ID and a secret access key. These should be stored securely and kept confidential.

For **Unix/Linux/macOS**:

- Configure your local AWS credentials file, typically located at `~/.aws/credentials`, by adding the following entries:

  ```
  [default]
  aws_access_key_id = YOUR_ACCESS_KEY_ID
  aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
  ```

- For the AWS configuration file, usually at `~/.aws/config`, set your default region if desired:

  ```
  [default]
  region = us-east-1
  ```

  **For Unix/Linux/macOS and Windows using Bash:**

- Open your terminal or Bash and set the environment variables using the `export` command. Replace `YOUR_ACCESS_KEY_ID` and `YOUR_SECRET_ACCESS_KEY` with your actual AWS credentials.

   ```bash
   export AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
   export AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
   ```
Optionally, you can also set the default AWS region:

```
export AWS_DEFAULT_REGION=us-east-1
```

For **Windows**:

- AWS credentials should be placed in the file located at `C:\Users\USERNAME\.aws\credentials`, where `USERNAME` is your Windows username, with the following format:

  ```
  [default]
  aws_access_key_id = YOUR_ACCESS_KEY_ID
  aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
  ```

- Similarly, set the default region in `C:\Users\USERNAME\.aws\config`:

  ```
  [default]
  region = us-east-1
  ```
  **For Windows using PowerShell:**

- In PowerShell, you can set the environment variables using the following commands. Again, replace the placeholders with your actual AWS credentials.

```
$env:AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"
$env:AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"
```

And to set the default region in PowerShell:

```
$env:AWS_DEFAULT_REGION="us-east-1"
```

- In both cases, if you are not using the default profile or if you have multiple AWS profiles, you can create or update a different profile by changing `[default]` to, for example, `[myprofile]`. Remember to configure your application to use the correct profile.

- These credentials allow your application to authenticate its requests to AWS and must be kept secure to prevent unauthorized access to your AWS resources.


### Configuration

- Update the `BUCKET_NAME` in the application with the name of your S3 bucket.

### Running the Application

1. Start the Flask server:
```
python app.py
```

2. Navigate to `http://localhost:5000` in your web browser to access the application.

## Usage

1. Upload a supported document type (PNG, JPG, JPEG, PDF, DOC, DOCX) through the web interface.
2. Wait for the document to be processed. The application will display the extracted text once it's available.

## Contributing

Contributions are welcome. Please open an issue first to discuss your proposal.

## License

Specify your license.

## Acknowledgments

- AWS Textract for providing the text extraction service.
- Flask for the web framework.


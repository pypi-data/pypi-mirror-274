# s3_tool

A tool for uploading and downloading files and folders to/from S3 with progress indication and file existence checks.

## Installation

To install the package, run:

```sh
pip install s3_tool
```

During installation, you will be prompted to enter your AWS credentials, which will be stored for future use.

## Features
- Upload files and folders to S3
- Download files and folders from S3
- Check if a file exists before uploading or downloading
- Display progress bar for file uploads and downloads

## AWS Credentials
This tool requires AWS credentials to access S3. During the installation, you will be prompted to enter your AWS Access Key ID, AWS Secret Access Key, and AWS Region. These credentials will be stored in `~/.aws/credentials` for future use.

## Usage
### Upload
**Upload a single file**

To upload a single file to S3, run:

```sh
s3-upload /path/to/local/file bucket_name s3/path/to/destination --region your-aws-region
```

Example:
```sh
s3-upload /path/to/local/file.txt my-bucket my-folder/file.txt --region us-east-1
```
**Upload a folder**
To upload a folder to S3, run:

```sh
s3-upload /path/to/local/folder bucket_name s3/path/to/destination --region your-aws-region
```

Example:
```sh
s3-upload /path/to/local/folder my-bucket my-folder --region us-east-1
```

### Download
**Download a single file**

To download a single file to S3, run:

```sh
s3-download bucket_name s3/path/to/source /path/to/local/destination --region your-aws-region
```

Example:
```sh
s3-download my-bucket my-folder/file.txt /path/to/local/file.txt --region us-east-1
```
**Download a folder**
To download a folder to S3, run:

```sh
s3-download bucket_name s3/path/to/source/ /path/to/local/destination --region your-aws-region
```

Example:
```sh
s3-download my-bucket my-folder/ /path/to/local/folder --region us-east-1
```

### Notes
- The tool will check if a file exists in the destination before uploading or downloading. If the file already exists, it will skip the operation and print a message.
- A progress bar will be displayed during the upload and download of files and folders.

## Author
Manuel Rodriguez Ladron de Guevara
import os
import boto3
import argparse
from pathlib import Path
import configparser
from tqdm import tqdm

def load_aws_credentials():
    config_path = Path.home() / '.aws' / 'credentials'
    if not config_path.exists():
        raise FileNotFoundError("AWS credentials file not found. Please run the installation script again.")
    
    config = configparser.ConfigParser()
    config.read(config_path)
    aws_credentials = config['default']

    os.environ['AWS_ACCESS_KEY_ID'] = aws_credentials['AWS_ACCESS_KEY_ID']
    os.environ['AWS_SECRET_ACCESS_KEY'] = aws_credentials['AWS_SECRET_ACCESS_KEY']
    os.environ['AWS_REGION'] = aws_credentials['AWS_REGION']

def upload_file_to_s3(local_file_path, bucket_name, s3_file_path, region_name='us-east-1'):
    load_aws_credentials()
    s3_client = boto3.client('s3', region_name=region_name)
    
    if s3_file_exists(bucket_name, s3_file_path):
        print(f"File {s3_file_path} already exists in s3://{bucket_name}. Skipping upload.")
        return
    
    file_size = os.path.getsize(local_file_path)
    
    with tqdm(total=file_size, unit='B', unit_scale=True, desc=local_file_path) as pbar:
        s3_client.upload_file(local_file_path, bucket_name, s3_file_path, Callback=ProgressPercentage(pbar))
    print(f"Uploaded {local_file_path} to s3://{bucket_name}/{s3_file_path}")

def download_file_from_s3(bucket_name, s3_file_path, local_file_path):
    load_aws_credentials()
    s3_client = boto3.client('s3')

    if os.path.exists(local_file_path):
        print(f"File {local_file_path} already exists locally. Skipping download.")
        return

    file_size = get_s3_file_size(bucket_name, s3_file_path)
    
    with tqdm(total=file_size, unit='B', unit_scale=True, desc=s3_file_path) as pbar:
        s3_client.download_file(bucket_name, s3_file_path, local_file_path, Callback=ProgressPercentage(pbar))
    print(f"Downloaded s3://{bucket_name}/{s3_file_path} to {local_file_path}")

def upload_folder_to_s3(local_folder, bucket_name, s3_folder, region_name='us-east-1'):
    load_aws_credentials()
    s3_client = boto3.client('s3', region_name=region_name)
    for root, dirs, files in os.walk(local_folder):
        for file in files:
            local_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_file_path, local_folder)
            s3_file_path = os.path.join(s3_folder, relative_path).replace("\\", "/")
            
            if s3_file_exists(bucket_name, s3_file_path):
                print(f"File s3://{bucket_name}/{s3_file_path} already exists. Skipping upload.")
                continue

            file_size = os.path.getsize(local_file_path)
            with tqdm(total=file_size, unit='B', unit_scale=True, desc=local_file_path) as pbar:
                s3_client.upload_file(local_file_path, bucket_name, s3_file_path, Callback=ProgressPercentage(pbar))
            print(f"Uploaded {local_file_path} to s3://{bucket_name}/{s3_file_path}")

def download_folder_from_s3(bucket_name, s3_folder_path, local_folder_path, region_name='us-east-1'):
    load_aws_credentials()
    s3_client = boto3.client('s3', region_name=region_name)
    s3_resource = boto3.resource('s3', region_name=region_name)
    bucket = s3_resource.Bucket(bucket_name)
    if not os.path.exists(local_folder_path):
        os.makedirs(local_folder_path)
    for obj in bucket.objects.filter(Prefix=s3_folder_path):
        s3_file_path = obj.key
        relative_path = os.path.relpath(s3_file_path, s3_folder_path)
        local_file_path = os.path.join(local_folder_path, relative_path)

        if os.path.exists(local_file_path):
            print(f"File {local_file_path} already exists locally. Skipping download.")
            continue

        file_size = obj.size
        with tqdm(total=file_size, unit='B', unit_scale=True, desc=s3_file_path) as pbar:
            bucket.download_file(s3_file_path, local_file_path, Callback=ProgressPercentage(pbar))
        print(f"Downloaded s3://{bucket_name}/{s3_file_path} to {local_file_path}")

def s3_file_exists(bucket_name, s3_file_path):
    s3_client = boto3.client('s3')
    try:
        s3_client.head_object(Bucket=bucket_name, Key=s3_file_path)
        return True
    except:
        return False

def get_s3_file_size(bucket_name, s3_file_path):
    s3_client = boto3.client('s3')
    response = s3_client.head_object(Bucket=bucket_name, Key=s3_file_path)
    return response['ContentLength']

class ProgressPercentage:
    def __init__(self, pbar):
        self._pbar = pbar

    def __call__(self, bytes_amount):
        self._pbar.update(bytes_amount)

def upload_command():
    parser = argparse.ArgumentParser(description="Upload files/folders to S3")
    parser.add_argument("local_path", help="Local file or folder path")
    parser.add_argument("bucket", help="S3 bucket name")
    parser.add_argument("s3_path", help="S3 destination path")
    parser.add_argument("--region", default="us-east-1", help="AWS region")
    args = parser.parse_args()

    if os.path.isdir(args.local_path):
        upload_folder_to_s3(args.local_path, args.bucket, args.s3_path, args.region)
    else:
        upload_file_to_s3(args.local_path, args.bucket, args.s3_path, args.region)

def download_command():
    parser = argparse.ArgumentParser(description="Download files/folders from S3")
    parser.add_argument("bucket", help="S3 bucket name")
    parser.add_argument("s3_path", help="S3 source path")
    parser.add_argument("local_path", help="Local destination path")
    parser.add_argument("--region", default="us-east-1", help="AWS region")
    args = parser.parse_args()

    if args.s3_path.endswith('/'):
        download_folder_from_s3(args.bucket, args.s3_path, args.local_path, args.region)
    else:
        download_file_from_s3(args.bucket, args.s3_path, args.local_path)

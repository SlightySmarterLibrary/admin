import boto3 as b3

AWS_REGION = 'us-east-1'
AWS_S3_BUCKET_NAME = 'team8-slightly-smarter-library'

# Create Client
s3 = b3.client('s3', region_name=AWS_REGION)

# Create bucket with default parameters
response = s3.create_bucket(
    ACL='public-read',
    Bucket=AWS_S3_BUCKET_NAME,
)

print("S3 setup completed")
print(
    f"Bucket name: {AWS_S3_BUCKET_NAME} \nBucket Location: {response['Location']}")

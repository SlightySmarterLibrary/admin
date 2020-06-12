import boto3 as b3
from PIL import Image
import io

AWS_S3_BUCKET_NAME = 'team8-slightly-smarter-library'
AWS_REGION = 'us-east-1'

s3 = b3.client('s3', region_name=AWS_REGION)


def upload_book_qr_code(id, qr_code, user_id, bucket=AWS_S3_BUCKET_NAME):
    """Uploads a book's QR code to S3 and returns its path on S3"""
    try:
        # Format the file for upload to S3.
        in_mem_image = io.BytesIO()
        qr_code.save(in_mem_image, format=qr_code.format)
        in_mem_image.seek(0)

        # Specify Key
        key = f"{user_id}/{id}.png"

        s3.put_object(
            ACL='public-read',
            Body=in_mem_image,
            Bucket=AWS_S3_BUCKET_NAME,
            Key=key,
            Metadata={
                'user_id': user_id,
            },
        )

        return f"https://{AWS_S3_BUCKET_NAME.lower()}.s3.amazonaws.com/{key}"
    except Exception as e:
        print(e)

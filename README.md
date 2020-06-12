# Admin
Web app for the Slighty Smarter Library

### Note:
We used `django-warrant` in order to do
authentication with AWS Cognito. However,
`django-warrant` is no longer maintained.

To fix this:
- We downloaded the
[latest version](https://github.com/MetaMetricsInc/django-warrant)
from Github.
 - We copied the files in the `django_warrant`
 folder to a new app folder in Django.
    ```
    python manage.py startapp djwarrant
    ```
 - Some edits in the files were made in order
to accommodate Django 2.1.1 (which is what we used
so that it works with AWS Elastic BeanStalk)

## Setup
1. Add your AWS credentials to your `.aws` file on your computer.
2. Run the Python file that setups up the various AWS service you need for the project.
   - Cognito: The identity pool, etc.
      - `python3 utils/setupCognito.py`
   - Dynamo: Tables required for the app. This only setups the table. I will add the index themselves later.
      - `python3 utils/setupDynamoTables.py`
   - S3: The public bucket to store the qr_code
      - `python3 utils/setupS3.py`

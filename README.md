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
1. Add your AWS credentials to your `.aws` file on your computer and it to the `settings.py` file.
2. Create User Pool, User Pool App Client, and Identify Pools called `maskidentity`.
   - The app client should then be linked to the user identity pool.
3. Create DynamoDB Tables
   - The `Stores` table is automatically created when the first user signs up.
   - The `Orders` table is created with various parameters and must have an index called `store_id-index` with `store_id` as the Partition Key.
4. Upload to Elastic BeanStalk
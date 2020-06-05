import boto3 as b3

AWS_REGION = 'us-east-1'
COGNITO_NAME = 'admin'
setup_exists_already = False

# Create Client
cognitoIDP = b3.client('cognito-idp', region_name=AWS_REGION)

# Check if there's an existing pool.
for user_pool in cognitoIDP.list_user_pools(MaxResults=5)['UserPools']:
    if user_pool['Name'] == COGNITO_NAME:
        setup_exists_already = True

if not setup_exists_already:
    # Create user Pool
    pool = cognitoIDP.create_user_pool(
        PoolName=COGNITO_NAME,
        Policies={
            'PasswordPolicy': {
                'MinimumLength': 10,
                'RequireUppercase': False,
                'RequireLowercase': False,
                'RequireNumbers': False,
                'RequireSymbols': False,
                'TemporaryPasswordValidityDays': 123
            }
        },
        AutoVerifiedAttributes=['email'],
        Schema=[
            {
                'Name': 'name',
                'AttributeDataType': 'String',
                'DeveloperOnlyAttribute': False,
                'Mutable': True,
                'Required': True,
            },
            {
                'Name': 'email',
                'AttributeDataType': 'String',
                'DeveloperOnlyAttribute': False,
                'Mutable': True,
                'Required': True,
            },
            {
                'Name': 'preferred_username',
                'AttributeDataType': 'String',
                'DeveloperOnlyAttribute': False,
                'Mutable': True,
                'Required': False,
            }
        ],
        UsernameConfiguration={
            'CaseSensitive': False
        },
    )

    # Create Pool Client
    userPoolId = pool['UserPool']['Id']

    poolClient = cognitoIDP.create_user_pool_client(
        UserPoolId=userPoolId,
        ClientName=COGNITO_NAME,
        GenerateSecret=False,
        RefreshTokenValidity=7,
        ReadAttributes=[
            'address', 'birthdate', 'email', 'email_verified', 'family_name', 'gender', 'given_name', 'locale', 'middle_name', 'name', 'nickname', 'phone_number', 'phone_number_verified', 'picture', 'preferred_username', 'profile', 'updated_at', 'website', 'zoneinfo'
        ],
        WriteAttributes=[
            'address', 'birthdate', 'email', 'family_name', 'gender', 'given_name', 'locale', 'middle_name', 'name', 'nickname', 'phone_number', 'picture', 'preferred_username', 'profile', 'updated_at', 'website', 'zoneinfo'
        ],
        SupportedIdentityProviders=['COGNITO'],
        ExplicitAuthFlows=[
            'ALLOW_CUSTOM_AUTH', 'ALLOW_USER_SRP_AUTH', 'ALLOW_REFRESH_TOKEN_AUTH'
        ],
    )

    # Create Identity Pool Client
    cognitoIdentityClient = b3.client(
        'cognito-identity', region_name=AWS_REGION)
    userPoolClientId = poolClient['UserPoolClient']['UserPoolId']

    response = cognitoIdentityClient.create_identity_pool(
        IdentityPoolName=COGNITO_NAME,
        AllowUnauthenticatedIdentities=False,
        AllowClassicFlow=True,
        CognitoIdentityProviders=[
            {
                'ProviderName': f"cognito-idp.{AWS_REGION}.amazonaws.com/{userPoolId}",
                'ClientId': 'userPoolClientId',
                'ServerSideTokenCheck': True
            },
        ],
    )

    print('Fully setup Cognito User Pools and Identity Pools')

else:
    print('A set of pools already exists.')

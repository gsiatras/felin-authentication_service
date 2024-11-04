import boto3
from botocore.exceptions import ClientError
from config import cognito_client  # Import the initialized cognito_client

def get_user_info(access_token):
    """Fetch user information from AWS Cognito using the provided access token."""
    try:
        print('Getting info from token')
        user_info = cognito_client.get_user(AccessToken=access_token)
        return user_info
    except ClientError as e:
        print(f"Error getting user info: {e.response['Error']['Message']}")
        raise

def extract_user_id(user_info):
    """Extract user Cognito ID (sub) from the user info response."""
    user_cognito_id = None
    for attribute in user_info['UserAttributes']:
        if attribute['Name'] == 'sub':
            user_cognito_id = attribute['Value']
            break

    if not user_cognito_id:
        raise ValueError('Unable to retrieve user sub from Cognito.')
    
    print(f"User sub (Cognito ID) found: {user_cognito_id}")
    return user_cognito_id

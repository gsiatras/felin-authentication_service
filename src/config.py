import os
import boto3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration for AWS Cognito
COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
COGNITO_REGION = os.getenv('COGNITO_REGION')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')

# Initialize the Cognito client
cognito_client = boto3.client('cognito-idp', region_name=COGNITO_REGION)

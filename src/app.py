from flask import Flask, jsonify, request
from cognito_utils import get_user_info, extract_user_id
from db_utils import get_user_connection_mode, update_user_connection_mode, get_user_id_by_sub, upsert_trader, get_user_verification_status
# from botocore.exceptions import ClientError
# import logging

# logging.basicConfig(level=logging.DEBUG)  # Set the logging level
# logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for Application Load Balancer (ALB).
    This is used to check if the application is running and healthy.

    Returns:
        json: A JSON response with a status of 'healthy' and a 200 status code.
    """
    return jsonify({'status': 'healthy'}), 200



@app.route('/verify-merchant', methods=['GET'])
def verify_merchant():
    """
    Verifies if a user is a registered merchant (supplier).
    The user is verified based on the 'connection_mode' in the database,
    which is checked against the 'supplier' or 'both' modes.
    Additionally, checks the 'verification_status' to see if the user is fully verified.

    Args:
        access_token (str): Access token sent in the request URL's query parameters.

    Returns:
        json: A JSON response indicating whether the user is a valid supplier.
            - Success: Contains a message and the Cognito user ID (sub).
            - Error: A message indicating failure or lack of verification, with a relevant error code.
    """
    # Extract the access token from the API call
    access_token = request.args.get('access_token')

    if not access_token:
        return jsonify({'error': 'Access token is required'}), 400

    try:
        # Get the user information from Cognito using the access token
        user_info = get_user_info(access_token)
        # Extract the user's Cognito ID (sub) from the response
        user_cognito_id = extract_user_id(user_info)

        # Get user's connection_mode from the database
        connection_mode = get_user_connection_mode(user_cognito_id)
        # Get user's verification_status from the database
        verification_status = get_user_verification_status(user_cognito_id)

        # Check if the user is a supplier or both
        if connection_mode not in ['supplier', 'both']:
            return jsonify({'message': 'User not applied'}), 200

        # Check if the user is fully verified
        if verification_status != 'full':
            return jsonify({'message': 'User not verified yet'}), 200

        # If both conditions are met, return success
        return jsonify({'message': 'User verified successfully', 'cognito_id': user_cognito_id}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except ClientError as e:
        return jsonify({'error': f"Error interacting with Cognito: {e.response['Error']['Message']}"}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/new_merchant', methods=['POST'])
def new_merchant():
    """
    Registers a new merchant by adding or updating their details in the database.
    This endpoint requires the user to be authenticated with Cognito, and their
    access token should be included in the request's body. The user information
    is used to either insert or update the merchant's details in the 'trader' table.

    Args:
        access_token (str): The Cognito access token, which is required to authenticate the user.
        companyName (str): The name of the company/merchant.
        afm (str): The Greek tax identification number (AFM) of the company.
        address (str): The address of the merchant.
        businessType (str): The type of business/occupation.
        postalCode (str): The postal code of the merchant's location.
        city (str): The city where the merchant operates.
        phoneNumber (str): The phone number of the merchant.

    Returns:
        json: A JSON response with a message confirming the registration or update.
            - Success: Contains the Cognito user ID (sub) and the trader type (e.g., 'supplier' or 'both').
            - Error: A message indicating failure, with an error code.
    """
    # Extract the access token from the request
    access_token = request.json.get('access_token')

    if not access_token:
        return jsonify({'error': 'Access token is required'}), 400

    try:
        # Verify user with Cognito and get user info
        user_info = get_user_info(access_token)
        user_sub = extract_user_id(user_info)

        # Retrieve user_id from the "user" table using user_sub
        user_id = get_user_id_by_sub(user_sub)

        # Check for user's existing entry in the "trader" table and update or add new entry
        trader_data = {
            'user_id': user_id,
            'name': request.json.get('companyName'),
            'afm': request.json.get('afm'),
            'address': request.json.get('address'),
            'occupation': request.json.get('businessType'),
            'zipcode': request.json.get('postalCode'),
            'city': request.json.get('city'),
            'phone1': request.json.get('phoneNumber')
            # Add any other fields as needed
        }

        # Insert/update trader data
        trader_type = upsert_trader(user_id, trader_data)

        # Retrieve user's connection mode from the "user" table
        connection_mode = get_user_connection_mode(user_sub)

        # Update the connection mode if needed
        if connection_mode == 'customer':
            update_user_connection_mode(user_id, 'both')
        elif connection_mode == 'supplier':
            trader_type = 'supplier'

        return jsonify({
            'message': 'User updated successfully',
            'cognito_id': user_sub,
            'trader_type': trader_type
        }), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except ClientError as e:
        return jsonify({'error': f"Error interacting with Cognito: {e.response['Error']['Message']}"}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

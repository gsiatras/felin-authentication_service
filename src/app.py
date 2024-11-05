from flask import Flask, jsonify, request
from cognito_utils import get_user_info, extract_user_id
from db_utils import get_user_connection_mode
from botocore.exceptions import ClientError

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for ALB."""
    return jsonify({'status': 'healthy'}), 200

@app.route('/verify-merchant', methods=['GET'])
def verify_merchant():
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

        if connection_mode in ['supplier', 'both']:
            return jsonify({'message': 'User verified successfully', 'cognito_id': user_cognito_id}), 200
        else:
            return jsonify({'error': 'User is not a supplier'}), 403

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except ClientError as e:
        return jsonify({'error': f"Error interacting with Cognito: {e.response['Error']['Message']}"}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

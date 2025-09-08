from flask import request
from auth.utils import decode_token

def get_user_id_from_token():
    """Extract user ID from JWT token"""
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token[7:]  # Remove 'Bearer ' prefix
        user_id = decode_token(token)
        return user_id
    return None
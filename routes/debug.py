from flask import Blueprint, jsonify, request
from flask_login import current_user

debug_bp = Blueprint('debug', __name__, url_prefix='/debug')

@debug_bp.route('/current_user')
def current_user_info():
    """Return JSON with current_user status and request cookie info.
    Only for local debugging on localhost/127.0.0.1."""
    # Restrict to local requests only for safety
    remote = request.remote_addr
    if remote not in ('127.0.0.1', '::1', 'localhost'):
        return jsonify({'error': 'Debug endpoint only available from localhost', 'remote_addr': remote}), 403

    user_info = {
        'is_authenticated': current_user.is_authenticated,
        'username': getattr(current_user, 'username', None) if current_user.is_authenticated else None,
        'role': getattr(current_user, 'role', None) if current_user.is_authenticated else None,
        'user_id': getattr(current_user, 'id', None) if current_user.is_authenticated else None,
        'remote_addr': remote,
        'cookies': {k: v for k, v in request.cookies.items()}
    }
    return jsonify(user_info)

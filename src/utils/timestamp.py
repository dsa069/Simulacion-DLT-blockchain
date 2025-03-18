def get_current_timestamp():
    from datetime import datetime
    return datetime.utcnow().isoformat() + 'Z'
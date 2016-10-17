import os

_DEFAULT_DB = "sqlite:///proto.db"
_DEFAULT_CLIENT_SECRET = "client_secret.json"
_DEFAULT_APP_NAME = 'Gmail API Python Quickstart'

CLIENT_SECRET_FILE = os.environ.get("CLIENT_SECRET", _DEFAULT_CLIENT_SECRET)
APPLICATION_NAME = os.environ.get("APP_NAME", _DEFAULT_APP_NAME)
SQLITE_DB = os.environ.get("SQLITE_DB", _DEFAULT_DB)

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

__all__ = ["SQLITE_DB", "CLIENT_SECRET_FILE", "APPLICATION_NAME", "SCOPES"]

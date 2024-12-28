from pylord.middleware import Middleware
from pylord import app
import re
STATIC_TOKEN = "as4NhSk2"


class TokenMiddleware(Middleware):
    regex = re.compile(r"^Token: (\w+)$")

    def process_request(self, req):
        header = req.headers.get("Authorization", "")
        match = self.regex.match(header)
        token = match and match.group(1) or None
        req.token = token


class InvalidTokenException(Exception):
    pass


def on_exception(req, resp, exception):
    if isinstance(exception, InvalidTokenException):
        if req.token is None:
            resp.text = "Tokenni headersga qosh"
            resp.status_code = 401
        else:
            resp.text = "Token is Invalid"
            resp.status_code = 401




def login_required(handler):
    def wrapped_handler(req, resp, *args, **kwargs):
        token = getattr(req, "token", None)
        print(f"token:{token}")

        if token is None or token != STATIC_TOKEN:
            raise InvalidTokenException("Invalid Token")

        return handler(req, resp, *args, **kwargs)

    return wrapped_handler







"""LOCAL FAKE of google.genai.errors (rehearsal only)."""


class APIError(Exception):
    code = None


class ServerError(APIError):
    pass


class ClientError(APIError):
    pass

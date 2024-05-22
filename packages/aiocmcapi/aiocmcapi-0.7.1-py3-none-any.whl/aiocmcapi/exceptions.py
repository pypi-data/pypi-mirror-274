class ResponseDataError(Exception):
    def __init__(self, status: dict):
        super().__init__(f"CMC API Error {status['error_code']}: {status['error_message']}")

class EndpointNotFoundError(Exception):
    def __init__(self, endpoint: str):
        super().__init__(f"'{endpoint}' endpoint not found, json-parsed response have not 'status' key")
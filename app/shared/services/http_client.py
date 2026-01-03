import requests

from app.core.errors.exceptions import (
    AppException,
    NetworkError,
    UnauthorizedError,
    AccessDeniedError,
    NotFoundError,
    UnprocessableEntityError,
    ServerError,
    UnknownError,
    ValidationError,
)


class HttpClient:
    BASE_URL = "http://127.0.0.1:8000"

    def post(self, path: str, *, json: dict):
        try:
            response = requests.post(
                f"{self.BASE_URL}{path}",
                json=json,
                timeout=10,
            )
    
            status = response.status_code
    
            if status == 400:
                raise ValidationError(response.text)
    
            if status == 401:
                raise UnauthorizedError()
    
            if status == 403:
                raise AccessDeniedError()
    
            if status == 404:
                raise NotFoundError()
    
            if status == 422:
                raise UnprocessableEntityError(response.text)
    
            if status == 429:
                raise AccessDeniedError()
    
            if 500 <= status <= 599:
                raise ServerError()
    
            if not response.ok:
                raise UnknownError(response.text)
            if not response.content:
                return {}
    
            content_type = response.headers.get("Content-Type", "")
    
            if "application/json" in content_type:
                try:
                    return response.json()
                except ValueError:
                    return {}
    
            return {}
    
        except requests.ConnectionError:
            raise NetworkError()
    
        except AppException:
            raise
        
        except Exception as exc:
            raise UnknownError() from exc
    
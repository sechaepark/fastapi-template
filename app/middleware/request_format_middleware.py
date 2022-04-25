import json
import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, PlainTextResponse


class RequestFormatMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        print('#' * 80)
        print('middleware : RequestFormatMiddleware')
        print('#' * 80)

        if request.method in ('POST', 'PUT', 'PATCH'):
            if request.headers.get('content-type') != 'application/json':
                return PlainTextResponse(status_code=415)
        return await call_next(request)

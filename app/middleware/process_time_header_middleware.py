import json
import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class ProcessTimeHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        print('#' * 80)
        print('middleware : ProcessTimeHeaderMiddleware')
        print('#' * 80)
        start_time = time.time()
        res = await call_next(request)
        process_time = time.time() - start_time
        print(f'[{request.url}] process_time : {process_time}')
        res.headers['X-Process-Time'] = str(process_time)
        return res

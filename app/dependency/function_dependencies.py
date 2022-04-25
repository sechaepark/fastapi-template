from typing import Optional

from fastapi import Header, HTTPException, Depends, Cookie
from requests import session


async def get_header_token(x_token: str = Header(...)):
    print('$' * 80)
    print('dependency - get_header_token')
    print('$' * 80)

    if x_token != 'fake-super-secret-token':
        raise HTTPException(status_code=400, detail='X-Token header invalid')


async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {'q': q, 'skip': skip, 'limit': limit}


# # --------------------------------------------------------------------------------------------------------------------
# # Sub Dependency
def query_extractor(q: Optional[str] = None):
    return q


def query_or_cookie_extractor(q: str = Depends(query_extractor), last_query: Optional[str] = Cookie(None)):
    if not q:
        return last_query
    return q


# # --------------------------------------------------------------------------------------------------------------------
# # Dependency with yield
async def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

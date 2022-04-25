from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette import status

from dependency.function_dependencies import get_header_token

router = APIRouter(
    prefix='/admin',
    tags=['admin'],
    dependencies=[Depends(get_header_token)],
    responses={418: {'description': 'I am a teapot'}},
)


@router.get('/')
async def root():
    print('-' * 80)
    print('api router')
    print('-' * 80)
    return {'hello': 'admin'}


@router.post('/')
async def update_admin():
    return {'message': 'Admin getting schwifty'}

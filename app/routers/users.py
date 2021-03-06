from fastapi import APIRouter, Depends

from dependency.function_dependencies import get_header_token, common_parameters

router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[Depends(common_parameters)],
    responses={404: {'description': 'Not found'}},
)


@router.get('/', tags=['users'])
async def read_users():
    return [{'username': 'Rick'}, {'username': 'Morty'}]


@router.get('/me', tags=['users'])
async def read_user_me():
    return {'username': 'fakecurrentuser'}


@router.get('/{username}', tags=['users'])
async def read_user(username: str):
    return {'username': username}

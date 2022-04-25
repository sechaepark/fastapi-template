from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from dependency.common_query_params_dependency import CommonQueryParamsDependency
from dependency.function_dependencies import get_header_token, common_parameters

router = APIRouter(
    prefix='/items',
    tags=['items'],
    dependencies=[],
    responses={404: {'description': 'Not found'}},
)

fake_items_db = {'plumbus': {'name': 'Plumbus'}, 'gun': {'name': 'Portal Gun'}}


@router.get('/')
async def read_items():
    return fake_items_db


@router.get('/test1')
async def test1(commons: dict = Depends(common_parameters)):
    return commons


@router.get('/test2')
async def test2(commons: CommonQueryParamsDependency = Depends(CommonQueryParamsDependency)):
    print(commons.limit)
    return commons


@router.get('/test3')
async def test3(commons: CommonQueryParamsDependency = Depends()):
    return commons


@router.get('/{item_id}')
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail='Item not found')
    return {'name': fake_items_db[item_id]['name'], 'item_id': item_id}


@router.put('/{item_id}')
async def update_item(item_id: str):
    if item_id != 'plumbus':
        raise HTTPException(
            status_code=403, detail='You can only update the item: plumbus'
        )
    return {'item_id': item_id, 'name': 'The great Plumbus'}

import logging.config
import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware

from core.app_conf import app_conf
from core.app_meta import app_meta
from middleware.process_time_header_middleware import ProcessTimeHeaderMiddleware
from routers import users, items, oauth2, admin

logger = logging.getLogger('app.root')


def set_log():
    if not os.path.exists(app_meta.log_dir):
        os.mkdir(app_meta.log_dir)

    logging.config.dictConfig(config=app_conf.log)


def print_info():
    logger.info('*' * 80)
    logger.info('*' * 80)
    logger.info(f'Application Name : {app_conf.application.name}')
    logger.info(f'Application Version : {app_conf.application.version}')
    logger.info(f'Application Environment Variable : {app_conf.application.os_env_var}')
    logger.info(f'Application Environment : {app_conf.application.environment}')
    logger.info('-' * 80)
    logger.info('*' * 80)
    logger.info('*' * 80)
    logger.info('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))


def create_app():
    _app = FastAPI(
        title='FastAPI',
        description='',
        version='0.1.0',
        # terms_of_service='http://example.com/terms/',
        # contact={
        #     'name': 'Deadpoolio the Amazing',
        #     'url': 'http://x-force.example.com/contact/',
        #     'email': 'dp@x-force.example.com',
        # },
        # license_info={
        #     'name': 'Apache 2.0',
        #     'url': 'https://www.apache.org/licenses/LICENSE-2.0.html',
        # },
        # openapi_url='/openapi.json',
        # docs_url='/docs',
        # redoc_url='/redoc',
        # swagger_ui_oauth2_redirect_url='/docs/oauth2-redirect',
        dependencies=[]
    )

    _app.add_middleware(ProcessTimeHeaderMiddleware)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            'http://localhost',
            'http://localhost:8080',
        ],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    _app.include_router(users.router)
    _app.include_router(items.router)
    _app.include_router(admin.router)
    _app.include_router(oauth2.router)

    return _app


set_log()
print_info()
app = create_app()


@app.get('/', tags=['root'], response_class=FileResponse)
async def root():
    return './template/index.html'


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)

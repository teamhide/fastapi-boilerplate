import uvicorn
from core.config import get_config

if __name__ == '__main__':
    config = get_config()
    uvicorn.run(
        app='app:app',
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True if config.ENV != 'production' else False,
        workers=1 if config.ENV != 'production' else 2,
    )

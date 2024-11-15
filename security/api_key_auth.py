from fastapi.security import APIKeyHeader
from fastapi import Depends, HTTPException

from di_container import AppContainer

def create_api_key_auth():
    security = APIKeyHeader(name='X-API-KEY', auto_error=False)
    container = AppContainer()

    def global_api_key_auth(api_key: str = Depends(security)):
        print('api_key: ', api_key)
        print('env value: ', container.config.app.api_key())
        is_correct = api_key == container.config.app.api_key()
        if api_key is None or is_correct is False:
            raise HTTPException(status_code=401, detail='You are not authenticated')
        return True
    
    return global_api_key_auth
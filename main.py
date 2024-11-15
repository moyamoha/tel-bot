from dotenv import load_dotenv
from fastapi import FastAPI, Depends
import os
from tortoise.contrib.fastapi import register_tortoise
from di_container import AppContainer
from fastapi.middleware.cors import CORSMiddleware
from routers.nooha_router import router as nooha_router
from routers.category_router import category_router
from security.api_key_auth import create_api_key_auth


def create_app():
    load_dotenv()
    auth = create_api_key_auth()
    app = FastAPI(dependencies=[Depends(auth)])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],        # Allow all origins
        allow_credentials=False,      # Allow credentials (e.g., cookies, authorization headers)
        allow_methods=["*"],         # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],
    )
    app.include_router(nooha_router)
    app.include_router(category_router)
    register_tortoise(
        app,
        db_url=os.getenv('DB_URL'),
        modules={"models": ["models.nooha", "models.category", "models.nooha_category"]},
        generate_schemas=True,  # Set to True if you want Tortoise to create tables automatically
        add_exception_handlers=True,
    )
    return app

app = create_app()

@app.get("/")
def read_root():
    return {"Hello": "World"}

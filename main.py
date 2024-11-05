from typing import Union
from dotenv import load_dotenv
from fastapi import FastAPI, status, Depends, UploadFile
import boto3
import os
from tortoise.contrib.fastapi import register_tortoise
from services.nooha_storage import NoohaStorage
from dependency_injector.wiring import inject, Provide
from models.nooha import Nooha, NoohaCreate
from di_container import AppContainer
from fastapi.middleware.cors import CORSMiddleware


def create_app():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],        # Allow all origins
        allow_credentials=False,      # Allow credentials (e.g., cookies, authorization headers)
        allow_methods=["*"],         # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"], 
    )
    return app
 
app = create_app()
load_dotenv()

register_tortoise(
    app,
    db_url=os.getenv('DB_URL'),
    modules={"models": ["models.nooha", "models.category", "models.nooha_category"]},
    generate_schemas=True,  # Set to True if you want Tortoise to create tables automatically
    add_exception_handlers=True,
)



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/noohas/", status_code=status.HTTP_201_CREATED)
async def create_nooha(nooha: NoohaCreate):
    n = await Nooha.create(**nooha.model_dump())
    await n.save()
    return n

@app.put('/noohas/upload/{id}')
async def upload_nooha(id: str, file: UploadFile):
    n = await Nooha.get(id=id)
    nooha_storage = AppContainer().nooha_storage()
    try:
        key = nooha_storage.upload_nooha(file, nooha=n)
        n.aws_key = key
        await n.save()
    except Exception as e:
        print(e)

@app.get("/noohas/")
async def get_noohas():
    noohas = await Nooha.all()
    return noohas

@app.get("/noohas/{id}")
async def get_single_nooha(id: int):
    nooha = await Nooha.get(id=id)
    return nooha

@app.put("/noohas/{id}", status_code=status.HTTP_200_OK)
async def edit_nooha(id: int, nooha: NoohaCreate):
    n = await Nooha.get(id=id)
    await n.update_from_dict(nooha.dict()).save()
    return n

@app.delete("/noohas/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def get_single_nooha(id: int):
    n = await Nooha.get(id=id)
    await n.delete()


if __name__ == '__main__':
    container = AppContainer()
    container.init_resources()
    container.wire(modules=[__name__])
    print('YAHYA', os.getcwd())
    print(container.config())


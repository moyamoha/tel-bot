import boto3
from dependency_injector import containers, providers

from services.azure_storage import AzureBlobClient, AzureBlobClientConfig
from services.nooha_storage import NoohaStorage
from services.vimeo import VimeoClient


class AppContainer(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yaml"])
    
    nooha_storage = providers.Singleton(
        NoohaStorage,
        s3_client = providers.Singleton(
            boto3.client,
            "s3",
            aws_access_key_id=config.aws.access_key_id,
            aws_secret_access_key=config.aws.secret_access_key,
        )
    )

    vimeo_client = providers.Factory(
        VimeoClient,
        base_url=config.vimeo.base_url,
        token=config.vimeo.token,
    )

    azure_blob_client = providers.Factory(
        AzureBlobClient,
        config=providers.Factory(
            AzureBlobClientConfig,
            config.azure.blob_storage.account_key,
            config.azure.blob_storage.account_url,
        ),
        name=providers.Dependency(),
        file_type=providers.Dependency(),
    )

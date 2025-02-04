import boto3
from dependency_injector import containers, providers
from services.nooha_storage import NoohaStorage


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

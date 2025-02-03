from azure.storage.blob.aio import BlobClient
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import httpx
from dataclasses import dataclass


def get_container_name(file_type: str):
    match file_type:
        case "video":
            return "videos"
        case _:
            return None


@dataclass
class AzureBlobClientConfig:
    account_key: str
    account_url: str


class AzureBlobClient:
    """Note: After using this class, please close the client, using _close method to avoid memory issues"""

    def __init__(self, config: AzureBlobClientConfig, name: str, file_type: str):
        self.account_key = config.account_key
        self.account_url = config.account_url
        self.client = BlobClient(
            self.account_url,
            get_container_name(file_type),
            name,
            credential=self.account_key,
        )

    async def _close(self):
        if self.client:
            await self.client.close()

    async def exists(self):
        return await self.client.exists()

    async def get_metadata(self, key: str | None = None):
        metadata = (await self.client.get_blob_properties()).get("metadata")
        if key is None:
            return metadata
        if key in metadata:
            return metadata[key]
        else:
            raise Exception(f"No key-value pair found for {key} in blob's metadata")

    async def get_url(self) -> str:
        exists = await self.client.exists()
        if not exists:
            raise Exception("The blob doesn't exist")
        permission = BlobSasPermissions(read=True)
        expiry = datetime.utcnow() + timedelta(hours=24)
        sas = generate_blob_sas(
            account_name=str(self.client.account_name),
            container_name=self.client.container_name,
            blob_name=self.client.blob_name,
            account_key=self.account_key,
            expiry=expiry,
            permission=permission,
        )
        return f"{self.client.url}?{sas}"

    async def copy_from_url(self, url: str, metadata: dict[str, str] | None):
        result = await self.client.start_copy_from_url(
            url, metadata=metadata, requires_sync=True
        )
        is_success = (
            "copy_status" in result.keys() and result.get("copy_status") == "success"
        )
        if not is_success:
            raise Exception("Copying blob was not successful")

    async def upload(self, source_url: str, metadata: dict[str, str] | None):
        timeout = httpx.Timeout(None)
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "GET", source_url, follow_redirects=True, timeout=timeout
            ) as response:
                await self.client.upload_blob(response.aiter_bytes(), metadata=metadata)

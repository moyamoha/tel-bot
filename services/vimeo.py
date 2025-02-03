from box import Box
from dataclasses import dataclass
from httpx import AsyncClient


@dataclass
class VimeoVideo:
    title: str
    id: int
    download_link: str
    version_id: int


class VimeoClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.auth = {"Authorization": f"Bearer {token}"}

    @classmethod
    def vimeo_id_from_uri(cls, uri: str) -> int:
        parts = uri.split("/")
        last_part = parts[len(parts) - 1]
        return int(last_part)

    async def get_single_video(self, vimeo_id: int) -> VimeoVideo:
        async with AsyncClient() as client:
            resp = await client.get(
                url=f"{self.base_url}/me/videos/{vimeo_id}",
                headers=self.auth,
                params={
                    "fields": "name,download.link,download.size,metadata.connections.versions.current_uri",
                },
            )
            resp.raise_for_status()
            boxed = Box(resp.json())
            version = 0
            if hasattr(boxed.metadata.connections.versions, "current_uri"):
                version = self.__class__.vimeo_id_from_uri(
                    boxed.metadata.connections.versions.current_uri
                )
            video = VimeoVideo(
                boxed.name,
                vimeo_id,
                max(boxed.download, key=lambda rend: rend["size"]).link,
                version,
            )
            return video

    async def upload_from_url(self, source_url: str, video_title: str):
        async with AsyncClient() as client:
            payload = {
                "upload": {"approach": "pull", "link": source_url},
                "name": video_title,
            }
            resp = await client.post(
                url=f"{self.base_url}/me/videos",
                json=payload,
                headers=self.auth,
                params={"fields": "uri,name"},
            )
            resp.raise_for_status()
            return resp.json()

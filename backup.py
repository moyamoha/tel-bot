import asyncio
from datetime import datetime
from urllib.parse import quote

from httpx import HTTPStatusError

from di_container import AppContainer

async def backup(vimeo_id: int):
    blob_client = None
    app_container = AppContainer()
    print(app_container.config())
    try:
        vimeo = app_container.vimeo_client()
        video = await vimeo.get_single_video(vimeo_id)
        blob_client = app_container.azure_blob_client(
            name=str(vimeo_id), file_type="video"
        )
        already_exists = await blob_client.exists() and await blob_client.get_metadata(
            "version"
        ) == str(video.version_id)
        metadata = {
            "title": quote(video.title),
            "version": str(video.version_id),
        }
        result = ""
        if not already_exists:
            print(f'Started the upload for {vimeo_id} {datetime.now()}')
            await blob_client.upload(video.download_link, metadata)
            result = f"Video {vimeo_id} was backed up successfully {datetime.now()}\n"

        else:
            result = f"Video {vimeo_id} is already backed up. Reupload was skipped\n"
        return result
    except Exception as e:
        is_not_found_error = (
            isinstance(e, HTTPStatusError) and e.response.status_code == 404
        )
        if is_not_found_error:  # video doesn't exist in Vimeo, no need to try again
            msg = f"Video {vimeo_id} doesn't exist in Vimeo"
            print(msg)
        else:
            print(e)
    finally:
        if blob_client:
            await blob_client._close()

async def backup_list():
    _list = [
        1006484464,
        957764609,
        1026483227,
        1018645534,
        1008034849,
        1004094505,
        867404852,
        1026921528,
        946480188,
        1025371207,
        944847948,
        1018661972,
        949550173,
        1016059008,
        941200521,
        1008034979,
        1028871331,
        957707431,
        993469646,
        1027214548,
        944061684,
        1008035069,
        951837955,
        935759108,
        1022043442,
        955919705,
        953466204,
        935759213,
        1013054853,
        944049552,
        1026493843,
        951465370,
        953470375,
        1027405224,
        1026792875,
        1020145069,
    ]
    for vid in _list:
        result = await backup(vid)
        print(result)

if __name__ == "__main__":
    asyncio.run(backup_list())


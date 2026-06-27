import asyncio
from pathlib import Path
from instagrapi.types import Media
from app import igClient
from typing import Any, Callable, TypeVar, Union


_T = TypeVar("_T")

_ig_lock = asyncio.Lock()


async def _call_ig_client(func: Callable[..., _T], *args: Any, **kwargs: Any) -> _T:
    async with _ig_lock:
        return await asyncio.to_thread(func, *args, **kwargs)


async def download_reel(
    video_url: str,
    downloads_dir: Union[str, Path] = "downloads",
) -> tuple[Media, Path]:
    media_pk = await _call_ig_client(igClient.media_pk_from_url, video_url)
    media_info = await _call_ig_client(igClient.media_info, media_pk)
    downloaded_file_path = await _call_ig_client(
        igClient.video_download_by_url,
        media_info.video_url,
        str(media_pk),
        Path(downloads_dir),
    )

    return media_info, downloaded_file_path

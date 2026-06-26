import re

INSTAGRAM_URL_RE = re.compile(
    r"^(?:https?://)?(?:www\.)?instagram\.com/(?:[^/]+/)?(?:reel|p)/([^/?#&]+)",
    re.IGNORECASE,
)

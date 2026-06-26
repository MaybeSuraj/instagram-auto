from contextlib import suppress


def make_progress_callback(message, prefix: str, step: float = 5.0):
    last_progress_update = 0.0

    async def progress_callback(current, total):
        nonlocal last_progress_update
        if not total:
            return

        percentage = (current / total) * 100
        if percentage - last_progress_update >= step or percentage >= 100:
            last_progress_update = percentage
            with suppress(Exception):
                await message.edit_text(f"{prefix} {percentage:.2f}%")

    return progress_callback

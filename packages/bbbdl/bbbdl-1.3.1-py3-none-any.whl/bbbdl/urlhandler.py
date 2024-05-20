from typing import *
import re


playback_regex = re.compile(r"^(https?://.+)/playback/presentation/2\.0/playback\.html\?meetingId=([0-9a-f-]+)$")
"The regex used to parse BigBlueButton playback urls."


def playback_to_data(url: str) -> Sequence[str]:
    """
    Autodetect the base url and the meeting id from a BigBlueButton playback url.

    :return: The match groups of :data:`.playback_regex`.
    :raises ValueError: If the regex doesn't match.
    """
    match = playback_regex.match(url)
    if not match:
        raise ValueError("Could not split URL in base url and meeting id")
    return match.groups()

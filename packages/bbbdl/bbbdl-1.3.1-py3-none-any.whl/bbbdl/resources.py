from __future__ import annotations
from typing import *
import dataclasses
import requests
import bs4
import ffmpeg
from .urlhandler import playback_to_data
from .exc import MetadataNotFoundError, SourceNotFoundError


class Source:
    """
    A handler for the splitting of a single video source in multiple input nodes.

    It can be created by specifying an url pointing to a local or remote video.

    It is necessary because the same input source cannot be passed twice to ffmpeg.
    """

    def __init__(self, location: str):
        self.href: str = location
        self._video: Optional[ffmpeg.Stream] = None
        self._video_count: int = 0
        self._audio: Optional[ffmpeg.Stream] = None
        self._audio_count: int = 0

    def __repr__(self):
        return f"<{self.__class__.__qualname__} href={self.href} | videos={self._video_count} audios" \
               f"={self._audio_count}>"

    def __hash__(self):
        return hash(self.href)

    @classmethod
    def create_from_url(cls, href: str) -> Optional[Source]:
        """
        Check if a resource exists at an url, and create a :class:`.Source` from it if it does.

        :return: The created source.
        :raises SourceNotFoundError: If the request returned a non-2XX status code.
        """
        r = requests.head(href)
        if not (200 <= r.status_code < 300):
            raise SourceNotFoundError(f"HEAD for {href} returned {r.status_code}")
        return cls(location=href)

    def get_audio(self) -> ffmpeg.nodes.FilterableStream:
        """
        Get an input audio stream.

        :return: The created audio stream.
        """
        if self._audio is None:
            self._audio = ffmpeg.input(self.href).audio.asplit()
        self._audio_count += 1
        return self._audio.stream(self._audio_count)

    def get_video(self) -> ffmpeg.nodes.FilterableStream:
        """
        Get an input video stream.

        :return: The created video stream.
        """
        if self._video is None:
            self._video = ffmpeg.input(self.href).video.split()
        self._video_count += 1
        return self._video.stream(self._video_count)


@dataclasses.dataclass()
class Enable:
    """
    An object containing two timestamps relative to the start of a meeting.

    They represent the moments when a slide should be displayed and hidden from the screen.
    """

    start: float
    end: float


@dataclasses.dataclass()
class Slide:
    """
    An object representing a single slide from BigBlueButton.

    It contains the :class:`.Source` where the slide can be accessed, and a :class:`list` of :class:`Enable`,
    representing the moments when that slide is displayed on screen.
    """

    resource: Source
    enables: List[Tuple[float, float]]


@dataclasses.dataclass()
class Meeting:
    """
    An object representing all resources from a BigBlueButton meeting.
    """

    deskshare: Source
    "The :class:`.Source` for the desktop-sharing stream."

    webcams: Source
    "The :class:`.Source` for the presenter webcam stream."

    shapes: List[Slide]
    "A :class:`list` of all the :class:`.Slide` in the presentation."

    @classmethod
    def from_base_url(cls, base_url: str, meeting_id: str) -> Meeting:
        """
        Create a new :class:`.Meeting` from a BigBlueButton base url and a meeting id.

        :param base_url: The base url of the BigBlueButton instance.
        :param meeting_id: The id of the meeting to get the resources from.
        :return: The created meeting.
        :raises MetadataNotFoundError: If the metadata request returned a non-2XX status code.
        """

        r = requests.get(f"{base_url}/presentation/{meeting_id}/metadata.xml")
        if not 200 <= r.status_code < 300:
            raise MetadataNotFoundError(f"GET for {base_url}/presentation/{meeting_id}/metadata.xml returned {r.status_code}")

        deskshare = Source.create_from_url(href=f"{base_url}/presentation/{meeting_id}/deskshare/deskshare.mp4")
        webcams = Source.create_from_url(href=f"{base_url}/presentation/{meeting_id}/video/webcams.mp4")

        shape_soup = bs4.BeautifulSoup(requests.get(f"{base_url}/presentation/{meeting_id}/shapes.svg").text,
                                       "lxml")

        shapes: Dict[str, Slide] = {}
        for tag in shape_soup.find_all("image"):
            if not tag["in"]:
                raise ValueError("Tag has no 'in' parameter")
            if not tag["out"]:
                raise ValueError("Tag has no 'out' parameter")
            if not tag["xlink:href"]:
                raise ValueError("Tag has no 'xlink:href' parameter")

            url = tag["xlink:href"]
            if url not in shapes:
                shapes[url] = Slide(resource=Source(f"{base_url}/presentation/{meeting_id}/{url}"), enables=[])
            shapes[url].enables.append((tag["in"], tag["out"]))

        return cls(
            deskshare=deskshare,
            webcams=webcams,
            shapes=list(shapes.values())
        )

    @classmethod
    def from_url(cls, url: str) -> Meeting:
        """
        Create a new :class:`.Meeting` from any BigBlueButton url by autodetecting the base url and the meeting id.

        .. seealso:: :func:`.playback_to_data`
        """
        return cls.from_base_url(*playback_to_data(url))

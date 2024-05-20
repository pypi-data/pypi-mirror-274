from typing import Optional
import ffmpeg.nodes


class Tracks:
    """
    A container for video and audio tracks. It starts empty, and more tracks can be added with the :meth:`.overlay`
    and :meth:`.amerge` methods.
    """

    def __init__(self):
        self.video: Optional[ffmpeg.nodes.FilterableStream] = None
        self.audio: Optional[ffmpeg.nodes.FilterableStream] = None

    def overlay(self, other: ffmpeg.nodes.FilterableStream, **kwargs):
        """
        Overlay a new video track.
        """

        if self.video is None:
            self.video = other
        else:
            self.video = self.video.overlay(other, **kwargs)

    def amerge(self, other: ffmpeg.nodes.FilterableStream, **kwargs):
        """
        Merge a new audio track.
        """

        if self.audio is None:
            self.audio = other
        else:
            self.audio = ffmpeg.filter((self.audio, other), "amerge", **kwargs)

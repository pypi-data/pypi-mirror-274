from typing import *
import ffmpeg
from .resources import Meeting
from .tracks import Tracks


def compose_screensharing(meeting: Meeting, width: int, height: int) -> Tracks:
    """
    Create a stream composed by:

    * the webcam video
    * the deskshare video overlayed on the webcam video
    * the webcam audio

    All video streams will be scaled so they all have the same size.

    :param meeting: The meeting to create the stream from.
    :param width: The width of the video file.
    :param height: The height of the video file.
    :return: A :class:`.Tracks` object containing the video and audio tracks.
    """

    tracks = Tracks()

    if meeting.webcams:
        tracks.overlay(meeting.webcams.get_video().filter("scale", width, height).filter("setsar", 1, 1))
        tracks.amerge(meeting.webcams.get_audio())

    if meeting.deskshare:
        tracks.overlay(meeting.deskshare.get_video().filter("scale", width, height).filter("setsar", 1, 1))

    return tracks


def compose_lesson(meeting: Meeting, width: int, height: int) -> Tracks:
    """
    Create a stream composed by:

    * the webcam video
    * the deskshare video overlayed on the webcam video
    * the slides images overlayed on the deskshare video when they are enabled
    * the webcam audio

    All video streams will be scaled so they all have the same size.

    :param meeting: The meeting to create the stream from.
    :param width: The width of the video file.
    :param height: The height of the video file.
    :return: A :class:`.Tracks` object containing the video and audio tracks.
    """

    tracks = compose_screensharing(meeting, width, height)

    for shape in meeting.shapes:
        scaled_split_shape = shape.resource.get_video().filter("scale", width, height).filter("setsar", 1, 1).split()
        count = 0
        for enable in shape.enables:
            count += 1
            tracks.overlay(scaled_split_shape.stream(count), enable=f"between(t, {enable[0]}, {enable[1]})")

    return tracks

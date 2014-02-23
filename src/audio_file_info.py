import os
from mutagen.m4a import M4A
from mutagen.mp3 import MP3


class UnsupportedFileError(IOError):
    pass


class AudioFileInfo(object):

    mime_to_mutagen_info = {"mp3": MP3, "m4a": M4A}

    def __init__(self, file_path):
        mutagen_info = self.mime_to_mutagen_info[self.get_ext_for(file_path)]
        if mutagen_info is None:
            raise UnsupportedFileError

        self.audio_info = mutagen_info(file_path)

    def get_ext_for(self, file_path):
        return os.path.splitext(file_path)[1].replace(".", "")

    def get_value_for(self, property):
        if property == "bitrate":
            return self.audio_info.info.bitrate

        if property == "genre":
            return self.audio_info.info.genre

        return ""

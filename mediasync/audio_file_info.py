import os

from mutagen.easyid3 import EasyID3
from mutagen.m4a import M4A


class UnsupportedFileError(IOError):
    pass


class MP3AudioInfo:

    def __init__(self, file_path):
        self.audio_info = EasyID3(file_path)

    def get_info(self):
        return str(self.audio_info.Get)

    def get_value_for(self, tag_name):
        if tag_name == "album":
            return self.audio_info["album"][0]

        if tag_name == "genre":
            try:
                return self.audio_info["genre"][0]
            except KeyError:
                pass

        return ""


class M4AAudioInfo:

    def __init__(self, file_path):
        self.audio_info = M4A(file_path)

    def get_info(self):
        return str(self.audio_info.tags)

    def get_value_for(self, tag_name):
        audio_tags = self.audio_info.tags
        try:
            if tag_name == "album":
                return audio_tags['\xa9alb']
            if tag_name == "genre":
                return audio_tags['\xa9gen']
        except(TypeError, KeyError):
            pass

        return ""


class MutagenFileInfoCreator(object):

    mime_to_mutagen_info = {"mp3": MP3AudioInfo, "m4a": M4AAudioInfo}

    def create(self, file_path):
        mutagen_info = self.get_mutagen_info_class_for(file_path)
        if mutagen_info is None:
            raise UnsupportedFileError
        return mutagen_info(file_path)

    def get_mutagen_info_class_for(self, file_path):
        mutagen_info = None
        ext = self.get_ext_for(file_path)
        if ext in self.mime_to_mutagen_info:
            mutagen_info = self.mime_to_mutagen_info[ext]
        return mutagen_info

    def get_ext_for(self, file_path):
        return os.path.splitext(file_path)[1].replace(".", "")

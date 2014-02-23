# coding=utf-8
import hashlib
import os
import sys

from audio_file_info import AudioFileInfo
from src.audio_file_info import UnsupportedFileError


class FileSync:
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.max_bitrate = 320
        self.genres_to_filter = "Practice"
        print "Copying from %s to %s ..." % (source, target)

    def sync(self):
        for root, dirs, filenames in os.walk(self.source):
            for f in filenames:
                f_path = os.path.join(root, f)
                if os.path.isfile(f_path):
                    try:
                        current_file_info = AudioFileInfo(f_path)
                        if self.audio_is_lossless(current_file_info) and \
                                self.genre_should_not_filtered(current_file_info) and \
                                self.file_is_different_from_target(f_path):
                            self.sync_file(os.path.join(root, f))
                            self.write(".")
                    except UnsupportedFileError:
                        self.write("-")

    def audio_is_lossless(self, audio):
        return audio.get_value_for("bitrate") <= self.max_bitrate

    def write(self, text):
        sys.stdout.write(text)
        sys.stdout.flush()

    def genre_should_not_filtered(self, audio):
        return not audio.get_value_for("genre") in self.genres_to_filter

    def file_is_different_from_target(self, file_path):
        target_file = self.get_target_file_for(file_path)
        if os.path.exists(target_file):
            self.write("@")
            return not self.files_are_same(file_path, target_file)

        return True

    def get_target_file_for(self, file_path):
        return os.path.join(self.get_target_path_for(file_path), os.path.basename(file_path))

    def get_target_path_for(self, file_path):
        return os.path.join(self.target, os.path.relpath(os.path.dirname(file_path), self.source))

    def files_are_same(self, file_path1, file_path2):
        return self.create_hash_for(file_path1) == self.create_hash_for(file_path2)

    def create_hash_for(self, file_path):
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                md5.update(chunk)
            return md5.digest()

    def sync_file(self, file_path):
        target_path = self.get_target_path_for(file_path)
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        os.system('cp "%s" "%s"' % (file_path, target_path))
        # shutil.copyfile(file_path, self.get_target_file_for(file_path))


if __name__ == "__main__":
    file_sync = FileSync(
        os.path.abspath("/Volumes/My Book TM/Backups.backupdb/Eli’s iMac/Latest/Lacie Extra/iTunes Music/Music"),
        os.path.abspath("/Volumes/Xtreamer_PRO/sda1/Music"))
    file_sync.sync()

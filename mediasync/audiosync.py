# coding=utf-8
import hashlib
import os
import shutil
import sys

from audio_file_info import AudioFileInfo
from audio_file_info import UnsupportedFileError


class FileSync:
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.max_bitrate = 320
        self.genres_to_filter = ["Practice", "Voice Memo"]
        self.files_to_ignore = ["._.DS_Store", ".DS_Store"]
        print "Copying from %s to %s ..." % (source, target)

    def sync(self):
        #self.delete_removed_files()
        print "Copying from %s to %s ..." % (self.source, self.target)
        for root, dirs, filenames in os.walk(self.source):
            for f in filenames:
                f_path = os.path.join(root, f)
                if os.path.isfile(f_path):
                    try:
                        current_file_info = AudioFileInfo(f_path)
                        if self.file_is_not_mp3_version(current_file_info) and \
                                self.genre_should_not_filtered(current_file_info) and \
                                self.file_is_different_from_target(f_path):
                            self.sync_file(os.path.join(root, f))
                            self.write(".")
                    except UnsupportedFileError:
                        self.write("-")

    def file_is_not_mp3_version(self, audio):
        return audio.get_value_for("album").find("mp3") == -1

    def audio_is_lossless(self, audio):
        return audio.get_value_for("bitrate") <= self.max_bitrate

    def write(self, text):
        sys.stdout.write(text)
        sys.stdout.flush()

    def genre_should_not_filtered(self, audio):
        for g in self.genres_to_filter:
            if audio.get_value_for("genre").find(g) != -1:
                return False
        return True

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
        return self.files_are_same_in_size(file_path1, file_path2) and \
            self.create_hash_from(AudioFileInfo(file_path1).get_info()) == self.create_hash_from(AudioFileInfo(file_path2).get_info())

    def files_are_same_in_size(self, file_path1, file_path2):
        return os.path.getsize(file_path1) == os.path.getsize(file_path2)

    def create_hash_for(self, file_path):
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
                md5.update(chunk)
            return md5.hexdigest()

    def sync_file(self, file_path):
        target_path = self.get_target_path_for(file_path)
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        os.system('cp "%s" "%s"' % (file_path, target_path))
        # shutil.copyfile(file_path, self.get_target_file_for(file_path))

    def create_hash_from(self, param):
        md5 = hashlib.md5()
        md5.update(param)
        return md5.hexdigest()

    def delete_removed_files(self):
        for root, dirs, file_names in os.walk(self.target):
            if not os.path.exists(os.path.join(self.source, root.replace(self.target, "").replace("/", "", 1))):
                shutil.rmtree(root)
            else:
                for f in file_names:
                    if not os.path.split(f)[1] in self.files_to_ignore and \
                            not os.path.exists(os.path.join(self.source, f)):
                        os.remove(os.path.join(self.target, f))


if __name__ == "__main__":
    file_sync = FileSync(
        os.path.abspath("/Volumes/Lacie Extra/iTunes Music/Music"),
        os.path.abspath("/Volumes/Music"))
    file_sync.sync()

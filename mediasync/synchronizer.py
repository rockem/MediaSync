import os

from file import OSFileOperator
from audio_file_info import MutagenFileInfoCreator


class Synchronizer(object):
    file_operator = OSFileOperator()
    file_info_creator = MutagenFileInfoCreator()
    filters = []

    def __init__(self, source_path, target_path):
        self.source_path = source_path
        self.target_path = target_path

    def sync(self):
        self.delete_files_from_target()
        self.copy_files_to_target()

    def delete_files_from_target(self):
        for f in self.file_operator.get_all_files_under(self.target_path):
            self.delete_from_target_if_not_in_source(f)

    def delete_from_target_if_not_in_source(self, file_path):
        if not self.file_operator.exists(self.file_path_in_source(file_path)):
            self.file_operator.delete(self.file_path_in_target(file_path))

    def file_path_in_source(self, song_file):
        return os.path.join(self.source_path, song_file)

    def file_path_in_target(self, song_file):
        return os.path.join(self.target_path, song_file)


    def copy_files_to_target(self):
        for f in self.file_operator.get_all_files_under(self.source_path):
            if not self.should_filter(f):
                self.copy_if_needed(f)

    def should_filter(self, f):
        for filter in self.filters:
            if filter.should_filter(self.file_info_creator.create(self.file_path_in_source(f))):
                return True
        return False

    def copy_if_needed(self, f):
        if self.target_file_has_same_size(f) or self.target_file_has_same_hash(f):
            self.copy_file_from_source_to_target(f)

    def target_file_has_same_size(self, f):
        return self.file_operator.getsize(self.file_path_in_source(f)) != self.file_operator.getsize(
            self.file_path_in_target(f))

    def target_file_has_same_hash(self, f):
        return self.file_info_creator.create(self.file_path_in_source(f)).hash() != self.file_info_creator.create(
            self.file_path_in_target(f)).hash()

    def copy_file_from_source_to_target(self, file_path):
        f_path = os.path.join(self.source_path, file_path)
        self.file_operator.copyfile(f_path, os.path.join(self.target_path, file_path))

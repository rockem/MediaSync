import os

from mockito import mock, when, verify, any, times, never

from mediasync.synchronizer import Synchronizer


class FileInfoCreatorStub(object):

    def __init__(self, file_to_info):
        self.file_to_info = file_to_info

    def create(self, file_path):
        return self.file_to_info[file_path]


class TestSynchronizer:
    SONG_FILE = "song.mp3"
    SOURCE_PATH = "source"
    TARGET_PATH = "target"

    file_list = []

    def setup(self):
        self.create_file_operator_mock()
        self.ms = Synchronizer(self.SOURCE_PATH, self.TARGET_PATH)
        self.ms.file_operator = self.file_operator_mock
        self.ms.file_info_creator = self.create_file_info_creator()

    def create_file_operator_mock(self):
        self.file_operator_mock = mock()
        when(self.file_operator_mock).get_all_files_under(any(str)).thenReturn([])
        when(self.file_operator_mock).exists(any(str)).thenReturn(False)
        when(self.file_operator_mock).getsize(any(str)).thenReturn(0)

    def create_file_info_creator(self):
        self.source_file_info_mock = mock()
        self.target_file_info_mock = mock()
        return FileInfoCreatorStub({
            self.file_path_in_source(self.SONG_FILE): self.source_file_info_mock,
            self.file_path_in_target(self.SONG_FILE): self.target_file_info_mock
        })

    def test_copy_song(self):
        self.create_file_in(self.SOURCE_PATH)
        self.ms.sync()
        self.verify_copy_file(self.SOURCE_PATH, self.TARGET_PATH)

    def verify_copy_file(self, source_path, target_path):
        verify(self.file_operator_mock).copyfile(os.path.join(source_path, self.SONG_FILE),
                                                 os.path.join(target_path, self.SONG_FILE))

    def file_path_in_target(self, song_file):
        return os.path.join(self.TARGET_PATH, song_file)

    def file_path_in_source(self, song_file):
        return os.path.join(self.SOURCE_PATH, song_file)

    def file_exists_in_target(self, file_path):
        return os.path.exists(self.file_path_in_source(file_path))

    def test_delete_target_if_needed(self):
        self.create_file_in(self.TARGET_PATH)
        self.ms.sync()
        verify(self.file_operator_mock).delete(self.file_path_in_target(self.SONG_FILE))

    def create_file_in(self, root, rel_path="", size=10):
        file_path = os.path.join(root, rel_path, self.SONG_FILE)
        when(self.file_operator_mock).get_all_files_under(root).thenReturn([os.path.join(rel_path, self.SONG_FILE)])
        when(self.file_operator_mock).exists(file_path).thenReturn(True)
        when(self.file_operator_mock).getsize(file_path).thenReturn(size)

    def test_skip_if_file_already_exists_in_the_same_size(self):
        self.create_file_in(self.TARGET_PATH)
        self.create_file_in(self.SOURCE_PATH)
        self.ms.sync()
        verify(self.file_operator_mock, times(0)).copyfile(any(str), any(str))

    def test_copy_if_file_exists_with_different_meta_hash(self):
        self.create_file_in(self.TARGET_PATH)
        self.create_file_in(self.SOURCE_PATH)
        when(self.source_file_info_mock).hash().thenReturn(123)
        when(self.target_file_info_mock).hash().thenReturn(1233)
        self.ms.sync()
        self.verify_copy_file(self.SOURCE_PATH, self.TARGET_PATH)

    def test_copy_song_in_hierarchy(self):
        sub_folder = "sub"
        self.create_file_in(self.SOURCE_PATH, sub_folder)
        self.ms.sync()
        self.verify_copy_file(os.path.join(self.SOURCE_PATH, sub_folder),
                              os.path.join(self.TARGET_PATH, sub_folder))

    def test_skip_song_if_any_filter_should_filter(self):
        self.create_file_in(self.SOURCE_PATH)
        f = mock()
        when(f).should_filter(any()).thenReturn(True)
        self.ms.filters = [f]
        self.ms.sync()
        verify(self.file_operator_mock, never).copyfile(any(), any())











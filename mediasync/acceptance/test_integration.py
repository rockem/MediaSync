import filecmp
import os
import shutil
from subprocess import call


class TestMain(object):
    SOURCE_PATH = "acceptance/test_data"
    TARGET_PATH = "target"

    def setup(self):
        os.mkdir(self.TARGET_PATH)

    def teardown(self):
        shutil.rmtree(self.TARGET_PATH)

    def test_copy_file_if_not_on_target(self):
        call(["python", "main.py", self.SOURCE_PATH, self.TARGET_PATH])
        self.assert_source_and_target_are_equals()

    def test_skip_copy_if_meta_is_the_same(self):
        pass

    def assert_source_and_target_are_equals(self):
        for root, dirs, file_names in os.walk(self.SOURCE_PATH):
            for f in file_names:
                if not filecmp.cmp(
                        os.path.join(root, f),
                        os.path.join(self.TARGET_PATH, os.path.relpath(root, self.SOURCE_PATH))):
                    return False

        return True

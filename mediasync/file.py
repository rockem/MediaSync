import os
import shutil


class OSFileOperator:

    def get_all_files_under(self, path):
        file_list = []
        for root, dirs, file_names in os.walk(path):
            for f in file_names:
                file_list.append(os.path.join(os.path.relpath(root, path), f))
        return file_list

    def copyfile(self, source, target):
        target_dir = os.path.dirname(target)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        shutil.copyfile(source, target)

    def exists(self, file_path):
        return os.path.exists(file_path)

    def delete(self, file_path):
        os.remove(file_path)

    def getsize(self, file_path):
        try:
            return os.path.getsize(file_path)
        except os.error:
            return -1
import os

from behave import *
from mutagen.easyid3 import EasyID3


use_step_matcher("re")


def find_mp3_file_in_source(context):
    for root, dirs, file_names in os.walk(context.source_path):
        for f in file_names:
            if os.path.splitext(f)[1] == ".mp3":
                return os.path.join(root, f)
    return ""


@given('There is a file with a \"(.*)\" genre exists in source')
def step_impl(context, genre):
    context.file_path = find_mp3_file_in_source(context)
    audio = EasyID3(context.file_path)
    audio["genre"] = genre
    audio.save()


@then("file should not exists in target")
def step_impl(context):
    assert not os.path.exists(context.file_path)

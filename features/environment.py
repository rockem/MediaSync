import os
import shutil

def before_all(context):
    context.source_path = "source"
    context.target_path = "target"
    shutil.copytree("test_data", context.source_path)


def before_feature(context, feature):
    os.mkdir(context.target_path)


def after_feature(context, feature):
    shutil.rmtree(context.target_path)


def after_all(context):
    shutil.rmtree(context.source_path)

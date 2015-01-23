import filecmp
import os
from subprocess import call

from behave import *

use_step_matcher("re")

@step("Target folder is empty")
def step_impl(context):
    pass


@step('I execute with parameters \"(.*)\"')
def step_impl(context, params):
    call(["python", "../mediasync/main.py"] + params.split(" "))


def is_source_and_target_are_equals(context):
    for root, dirs, file_names in os.walk(context.source_path):
        for f in file_names:
            if not filecmp.cmp(
                    os.path.join(root, f),
                    os.path.join(context.target_path, os.path.relpath(root, context.source_path), f)):
                return False

    return True


@then("Target and source folders should be identical")
def step_impl(context):
    assert is_source_and_target_are_equals(context)

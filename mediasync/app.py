from behave import runner
import click
import behave

from mediasync.filter import TagFilter
from synchronizer import Synchronizer


@click.command()
@click.option('--filter', multiple=True)
@click.argument('source')
@click.argument('target')
def main(source, target, filter):
    synchronizer = Synchronizer(source, target)
    synchronizer.filters = [TagFilter(f) for f in filter]
    synchronizer.sync()

if __name__ == "__main__":
    runner.
    main()
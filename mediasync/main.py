import click

from mediasynchronizer import MediaSynchronizer


@click.command()
@click.argument('source')
@click.argument('target')
def sync(source, target):
    MediaSynchronizer(source, target).sync()

if __name__ == "__main__":
    sync()
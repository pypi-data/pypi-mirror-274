# jzai/cli.py

import click
from .bot import run

@click.command()
def run():
    """Run the bot."""
    run()  # Call the main function of your bot

if __name__ == '__main__':
    run()

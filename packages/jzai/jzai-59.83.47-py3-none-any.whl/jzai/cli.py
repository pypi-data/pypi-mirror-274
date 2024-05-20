# jzai/cli.py

import click
from .bot import Bot

@click.command()
def run():
    """Run the bot."""
    bot = Bot(name="JZ")  # Initialize your Bot object
    bot.run()  # Call the run method of your Bot

if __name__ == '__main__':
    run()

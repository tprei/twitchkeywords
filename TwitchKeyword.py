from dotenv import load_dotenv
from twitchio.ext import commands
from typing import Coroutine

import inspect
import os

colors = {
    'GREEN':'\033[92m',
    'BOLD':'\033[1m',
    'BLUE':'\033[94m',
    'END':'\033[0m'
}

def colorize(string, color: str) -> str:
    """Colorize string"""
    return colors[color] + string + colors['END']

def get_credentials() -> tuple:
    """Gets bot auth credentials from environment variables defined in the local .env file"""

    load_dotenv()

    irc_token = os.environ.get('TWITCH_OAUTH_PASS')
    client_id = os.environ.get('TWITCH_CLIENT_ID')
    channel = os.environ.get('TWITCH_CHANNEL')

    return irc_token, client_id, channel

class TwitchAuthError(Exception):
    """Raised when auth variables are not properly configured"""
    pass

class Keyword(commands.Bot):
    """Twitch bot with support to custom keywords"""

    def __init__(self):
        irc, client, channel_name = get_credentials()

        if not irc or not client or not channel_name:
            raise TwitchAuthError(".env configuration file not properly configured.")

        # Connect to channel
        super().__init__(
                irc_token=irc,
                client_id=client,
                nick=channel_name,
                prefix='!',
                initial_channels=[channel_name],
        )

        self.keywords = {}

    async def event_ready(self):
        print(f'Connection successful. | Logged in as {self.nick}')
        print(f'_________________________________________________')
        print('')

    async def event_message(self, message):
        username = message.author.name
        content = message.content

        if content in self.keywords:
            self.loop.create_task(self.keywords[content]())
            content = colorize(content, "BLUE")

        print(f'{colorize(str(message.timestamp), "GREEN")} {colorize(username, "BOLD")}: {content}')

        await self.handle_commands(message)

    def add_keyword(self, name: str, action: Coroutine) -> None:
        """
        Method to add custom keywords to bot instance.

        Parameters
        ------------

        name: str [Required]
            string that must be sent in chat to trigger coroutine
        action: coro [Required] 
            coroutine to be executed when "name" is sent in chat

        Raises
        --------

        ValueError
            name must be str
            action must be coroutine function

        """
        
        if type(name) != str:
            raise ValueError('Name parameter must be str')

        if not inspect.iscoroutinefunction(action):
            raise ValueError('Action parameter must be coroutine')

        self.keywords[name] = action

if __name__ == '__main__':
    bot = Keyword()
    bot.run()


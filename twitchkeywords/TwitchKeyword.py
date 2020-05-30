from dotenv import load_dotenv
from twitchio.ext import commands
from typing import Coroutine

import inspect
import logging
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

        self._keywords = dict()
        self._prefixes = dict()
        self._suffixes = dict()
        self._contains = dict()

    async def event_message(self, message):
        username = message.author.name
        content = message.content
        color = False

        # Executing keyword bindings
        if content in self._keywords:
            # Executing coroutine tied to this keyword
            await self._keywords[content](message)
            color = True

        # Executing prefixes bindings
        for name, task in self._prefixes.items():
            if content.startswith(name):
                await task(message)
                color = True

        # Executing suffixes bindings
        for name, task in self._suffixes.items():
            if content.endswith(name):
                await task(message)
                color = True

        # Executing "contains" bindings
        for name, task in self._contains.items():
            if name in content:
                await task(message)
                color = True

        if color:
            content = colorize(content, "BLUE")

        print(f'{colorize(str(message.timestamp), "GREEN")} {colorize(username, "BOLD")}: {content}')

    @property
    def keywords(self):
        """Getter for keywords"""
        return self._keywords

    @keywords.setter
    def keywords(self, bindings):
        """Setter for keywords"""
        if type(bindings) != dict:
            raise ValueError('Wrong data type, must pass dictionary with tuples (str, coro).')
                
        self._keywords = bindings

    @property
    def prefix_keywords(self):
        """Getter for prefixes"""
        return self._prefixes

    @prefix_keywords.setter
    def prefix_keywords(self, bindings):
        """Setter for prefixes"""
        if type(bindings) != dict:
            raise ValueError('Wrong data type, must pass dictionary with tuples (str, coro).')
                
        self._prefixes = bindings

    @property
    def suffix_keywords(self):
        """Getter for suffixes"""
        return self._suffixes

    @suffix_keywords.setter
    def suffix_keywords(self, bindings):
        """Setter for suffixes"""
        if type(bindings) != dict:
            raise ValueError('Wrong data type, must pass dictionary with tuples (str, coro).')
                
        self._suffixes = bindings

    @property
    def contains_keywords(self):
        """Getter for contains"""
        return self._contains

    @contains_keywords.setter
    def contains_keywords(self, bindings):
        """Setter for contains"""
        if type(bindings) != dict:
            raise ValueError('Wrong data type, must pass dictionary with tuples (str, coro).')
                
        self._contains = bindings

    def set_keyword(self, name: str, action: Coroutine) -> None:
        """
        Associates keyword with coroutine

        Parameters
        ------------

        name: str [Required]
            string that must be sent in chat to trigger coroutine
        action: coro [Required] 
            coroutine to be invoked when name is sent in chat.

            **Note**: 
            Coroutine must take exactly one parameter with no default values, which is the message received.
            All other parameters **must** be default-valued parameters.

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

        self._keywords[name] = action

    def set_prefix(self, name: str, action: Coroutine) -> None:
        """
        Associates prefix with coroutine

        Parameters
        ------------

        name: str [Required]
            prefix to be associated with a coroutine
        action: coro [Required] 
            coroutine to be invoked when that certain prefix is seen in chat.

            **Note**: 
            Coroutine must take exactly one parameter with no default values, which is the message received.
            All other parameters **must** be default-valued parameters.

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

        self._prefixes[name] = action

    def set_suffix(self, name: str, action: Coroutine) -> None:
        """
        Associates suffix with coroutine

        Parameters
        ------------

        name: str [Required]
            suffix that must be seen in chat to invoke coroutine
        action: coro [Required] 
            coroutine to be invoked when suffix is seen in chat.

            **Note**: 
            Coroutine must take exactly one parameter with no default values, which is the message received.
            All other parameters **must** be default-valued parameters.

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

        self._suffixes[name] = action

    def set_contains(self, name: str, action: Coroutine) -> None:
        """
        Associates all messages that contain certain string with a coroutine

        Parameters
        ------------

        name: str [Required]
            string that must be inside a message sent in chat to trigger coroutine
        action: coro [Required] 
            coroutine to be invoked when name is sent in chat.

            **Note**: 
            Coroutine must take exactly one parameter with no default values, which is the message received.
            All other parameters **must** be default-valued parameters.

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

        self._contains[name] = action

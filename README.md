# Twitch Keywords Bot

A Twitch bot that handles commands and other features through the use of custom keywords.

## Installation

Clone this repository

`git clone https://github.com/tpreischadt/Twitch-Keywords.git`

Install all dependencies (it's heavily recommended that you do this inside a virtual enviroment).

`pip install -r requirements.txt`

## Authenticating

1) Go to https://twitchapps.com/tmi/ and get your **OAuth Password**. This is linked to your logged in account, so if you're planing on using bot-like features (such as sending messages in chat), you'd probably wanna do this within a bot account.

2) Go to the Twitch Developer Portal and register an **Application** to get your **Client ID** like so:

![registration](https://i.imgur.com/Wjdl0aD.png)

3) Create a `.env` file in the project's directory which looks like this:

![env](https://i.imgur.com/5uMd2PN.png)

And replace each value with your credentials. 

**IMPORTANT**: This is all sensitive information, do not share your OAuth Password, Client ID and/or .env file.

## Basic usage

Example code:

![example_code](https://i.imgur.com/iWrJOPk.png)

Here's a test in chat:

![twitch chat](https://i.imgur.com/obEQDDp.png)

Here's what the program's log will look like. Notice how when some message invokes a coroutine, it's colored blue.

![log](https://i.imgur.com/ObSO6w4.png)

#### For more advanced usage, you could create a class extending the Keywords class, which is a child class of TwitchIO's bot class. Nonetheless, I suggest not to override the on_message method, since that's what's handling the keywords/bindings coroutines invokations.

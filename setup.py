from pkg_resources import parse_requirements
from distutils.core import setup

setup(
  name = 'twitchkeywords',
  packages = ['twitchkeywords'],
  version = '0.1.2',
  license='MIT',
  description = 'Twitch bot that handles commands and other features through the use of custom keywords.',
  author = 'Thiago Preischadt',
  author_email = 'thiagopreischadt@gmail.com',
  url = 'https://github.com/tpreischadt/twitchkeywords',
  download_url = 'https://github.com/tpreischadt/twitchkeywords/archive/v0.1.tar.gz',
  keywords = ['twitch', 'keywords', 'bot'],
  install_requires =[
      "aiohttp",
      "asyncio",
      "twitchio"
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)

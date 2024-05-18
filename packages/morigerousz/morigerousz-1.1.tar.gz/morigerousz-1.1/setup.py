from distutils.core import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

setup(
    name = 'morigerousz',
    packages = ['morigerousz'],
    version = '1.1',
    license='MIT',
    description = 'morigerousz',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = 'Naistrai',
    author_email = 'rizkynaistrai@gmail.com',
    url = 'https://github.com/naistrai/morigerousz',
    download_url = 'https://github.com/naistrai/morigerousz/archive/v_01.tar.gz',
    project_urls={
        'Documentation': 'https://github.com/naistrai/morigerousz',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/naistrai/morigerousz/',
        'Tracker': 'https://github.com/naistrai/morigerousz/issues',
    },
    keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],
    install_requires=[
            'validators',
            'beautifulsoup4',
            'discordautochat',
            'discorudo',
        ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
     dependencies= [
        'discordautochat',
        'discorudo'
    ]
)

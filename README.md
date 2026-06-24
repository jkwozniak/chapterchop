# Chapterchop

[![License: GPL v2](https://img.shields.io/badge/License-GPL_v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![PyPI](https://img.shields.io/pypi/v/chapterchop)](https://pypi.org/project/chapterchop/)
[![Python](https://img.shields.io/pypi/pyversions/chapterchop)](https://pypi.org/project/chapterchop/)

Chapterchop — chop long audio into chapters as separate files convenient for offline listening.

> Chapterchop is currently in early development. The public API may evolve before the first stable 1.0 release.

## Table of Contents

- [About](#about)
    - [What is Chapterchop?](#what-is-chapterchop)
    - [When is it useful?](#when-is-it-useful)
- [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Install Chapterchop](#install-chapterchop)
- [Usage](#usage)
- [License](#license)


## About

### What is Chapterchop?

Chapterchop is both a command-line tool and Python library for splitting audio into chapters. It analyzes audio using a selected chaptering method, cuts the recording into individual segments, and exports the results as separate audio files.


### When is it useful?

This project was created for people who want to enjoy audio content available online without relying on a constant internet connection. Long-form content such as podcasts, audiobooks, and lectures is often easier to store and navigate when divided into chapters. Chapterchop helps automate this process.

You might find this tool useful if you:

- listen to podcasts, audiobooks, or music offline,
- prefer simple audio players over commercial streaming apps,
- need to split long recordings into smaller, easier-to-navigate chapters,
- want to archive long-form audio locally,
- use screenless sports MP3 players.


## Installation

### Prerequisites

- Python 3.11+
- ffmpeg


### Install Chapterchop

```bash
pip install chapterchop
```


## Usage

```bash
chapterchop split [-h] -i PATH -o PATH [-p N] [-v]
```

Options:
```
  -h, --help              Show this help message and exit
  -i PATH, --input PATH   Path to the input audio file

  -o PATH, --output PATH  Directory where output files will be written

  -p N, --parts N         Number of equally sized chapters to be created
  -v, --verbose           Show detailed processing information
```

Sample usage: split the audio file into five equal parts
```bash
chapterchop split -i input_file.mp3 -o ~/Desktop/output_dir -p 5 -v
```

## License

Released under the GPL-2.0-or-later license. See [LICENSE](LICENSE) for details.

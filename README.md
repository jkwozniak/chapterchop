# Chapterchop

[![License: GPL v2](https://img.shields.io/badge/License-GPL_v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![PyPI](https://img.shields.io/pypi/v/chapterchop)](https://pypi.org/project/chapterchop/)
[![Python](https://img.shields.io/pypi/pyversions/chapterchop)](https://pypi.org/project/chapterchop/)

Chapterchop — split long audio recordings into separate chapter files for offline listening.

> Chapterchop is currently in early development. The public API may evolve before the first stable 1.0 release.

## Table of Contents

- [About](#about)
    - [What is Chapterchop?](#what-is-chapterchop)
    - [When is it useful?](#when-is-it-useful)
- [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Install Chapterchop](#install-chapterchop)
- [Usage](#usage)
    - [Splitting methods](#splitting-methods)
    - [CLF files](#clf-files)
    - [Examples](#examples)
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

Chapterchop requires:

- Python 3.11 or later
- FFmpeg

#### FFmpeg

Chapterchop uses [FFmpeg](https://ffmpeg.org/) to read and process audio files.
FFmpeg is a free and open-source multimedia framework that supports a wide range
of audio and video formats.

If you do not have FFmpeg installed, follow the installation instructions for
your operating system in the [official FFmpeg documentation](https://ffmpeg.org/download.html).

After installing FFmpeg, verify that it is available by running:
```bash
ffmpeg -version
```

### Install Chapterchop
```bash
pip install chapterchop
```

## Usage

```bash
chapterchop split [--help] --input PATH --output PATH [--format FORMAT] [--parts N | --clf PATH] [--verbose]
```


### Splitting methods

Chapterchop supports two methods for splitting an audio file into chapters:

* **Equal parts** — use `--parts N` to divide the audio into `N` equally sized chapters. If no splitting method is specified, Chapterchop uses this method with 4 chapters by default.
* **CLF file** — use `--clf PATH` to split the audio according to chapter definitions provided in a [CLF file](https://github.com/jkwozniak/chapterchop/blob/main/docs/formats/clf-v1.md).

These options are mutually exclusive. A single `split` command can use either `--parts` or `--clf`, but not both.


### CLF files

A CLF (Chapter List Format) file is a text file that specifies the starting points of chapters in an audio recording. Each line contains a chapter start time in `HH:MM:SS` or `MM:SS` format, optionally followed by a chapter title.

For example:

```text
00:00 Introduction
00:30 Chapter One
03:00 Chapter Two
```

Use the file with the `--clf` option:

```bash
chapterchop split -i input_file.mp3 -o ./output_dir --clf chapters.clf
```

For the complete CLF specification, see the [CLF v1 format specification](https://github.com/jkwozniak/chapterchop/blob/main/docs/formats/clf-v1.md).


Options:
```text
options:
  -h, --help                   show this help message and exit
  -i PATH, --input PATH        path to the input audio file
  -o PATH, --output PATH       directory where output files will be written
  -f FORMAT, --format FORMAT   output audio format: 'wav' (default), 'mp3' or 'ogg'
  -p N, --parts N              number of equally sized chapters to be created (default: 4)
  --clf PATH                   path to the CLF file containing chapter information
  -v, --verbose                show detailed processing information
```

### Examples

**Split the audio file into four equal parts:**
```bash
chapterchop split -i input_file.mp3 -o .
```

**Split the audio file into 3 equal parts and export to the mp3 format:**
```bash
chapterchop split -i input_file.mp3 -o ./output_dir --parts 3 --format mp3
```

**Split the audio file into seven equal parts using verbose mode:**
```bash
chapterchop split -i input_file.mp3 -o ./output_dir --parts 7 --verbose
```

**Split audio based on a CLF file:**
```bash
chapterchop split -i input_file.mp3 -o ./output_dir --clf chapters.clf
```

## License

Released under the GPL-2.0-or-later license. See [LICENSE](https://github.com/jkwozniak/chapterchop/blob/main/LICENSE) for details.

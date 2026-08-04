# Chapter List File (CLF)

**Version**: 1

This document specifies the Chapter List File (CLF) format, including its syntax, semantics, and illustrative examples.

___

## What is CLF

CLF is a plain-text file format used by Chapterchop to represent chapter boundaries originating from external sources. CLF is designed to be minimal, human-readable, and intuitive.


## Syntax

CLF is a UTF-8 encoded text file without a BOM with the structure described below.


### Lexical conventions

- **space**: ASCII space (0x20)
- **digit**: any decimal digit (0–9)
- **title-character**: any Unicode character except newline
- **newline**: LF or CRLF
- **LF**: line feed (0x0A)
- **CR**: carriage return (0x0D)


### File structure (EBNF)
```ebnf
chapter-list = chapter-line ,                     (* at least one chapter is required *)
             { newline , chapter-line } ;         (* the remaining chapters are optional *)

chapter-line = timestamp                          (* chapter without a title *)
             | timestamp , separator , title ;    (* chapter with a title *)

timestamp = minutes ":" seconds
          | hours ":" minutes ":" seconds ;

seconds = digit , digit ;

minutes = digit , [ digit ] ;

hours = digit , [ digit ] ;

separator = space                                 (* "timestamp title" *)
          | space , "-" , space;                  (* "timestamp - title" *)

title = title-character , { title-character } ;   (* at least one character is required *)
```

### Semantic rules

- chapter timestamps are interpreted as chapter start positions,
- the values for each unit of time (h/m/s) must be within the range of 0 to 59,
- timestamp values must be strictly increasing,
- leading whitespace is not permitted,
- before syntactic analysis, trailing whitespace on each line is removed,
- chapter lines without a title produce `title = None`,
- blank lines are not permitted.

> A conforming CLF parser is expected to normalize the input according to the semantic rules above before constructing a ChapterList.


### Separator ambiguity

The format defines two variants of the separator between the timestamp and the title:
- short: ` ` (single space)
- long: ` - ` (space, dash, space)

Since a single space is a valid separator, any characters following the first space are treated as part of the chapter title, unless they form a long separator (" - ").

For example:
```
0:15 ~ Chapter 1
10:00 _ Chapter 2
```

are both valid CLF entries, but the titles become: `~ Chapter 1` and `_ Chapter 2` rather than `Chapter 1` and `Chapter 2`.

Although the entries above do not violate the formal rules of the format, this type of notation can be misleading and is therefore discouraged.
When using a long separator, always write it exactly as defined by the specification.


## Examples

### Valid example 1: uniformly formatted list
```
0:00:00 Introduction
0:00:57 Prerequisites
0:01:40 How to Take This Course
0:02:26 Getting Started with Docker
0:03:10 What is Docker?
0:06:25 Virtual Machines vs Containers
0:09:39 Docker Architecture
0:11:54 Installing Docker
0:15:29 Development Workflow
0:17:45 Docker in Action
0:27:54 The Linux Command Line
0:28:47 Linux Distributions
0:29:49 Running Linux
0:35:01 Managing Packages
0:38:35 Linux File System
0:40:33 Navigating the File System
0:44:53 Manipulating Files and Directories
0:48:20 Editing and Viewing Files
0:52:15 Redirection
```

### Valid example 2: various timestamp formats and a long separator
```
00:00 - Introduction
04:40 - History and motivation
30:27 - Technology overview
40:30 - Installation and set up
47:15 - Using 3rd party container images
48:06 - Understanding container data and docker volumes
1:13:00 - Demo application
1:28:37 - Building container images
2:23:46 - Container registries
2:33:45 - Running containers
3:02:36 - Container security
3:06:58 - Interacting with Docker objects
3:18:36 - Development workflow
3:52:05 - Ephemeral environments with Shipyard
4:07:17 - Deploying containers
4:42:59 - Final wrap up
```

### Valid example 3: list with a non-uniform line structure
```
00:00 - Intro
2:16 Track 1
3:54
4:00 Track 2
09:44
9:51 Track 3
14:17 Track 4
00:19:53 Track 5
0:25:04 - Bonus Track
```

### Invalid chapter-line examples:
```
00 Intro             # incorrect timestamp format
10:75 Chapter 1      # incorrect timestamp value
-> 15:35 Chapter 2   # characters preceding the timestamp
                     # empty line
20:00Chapter 3       # missing separator before the title
30:30>>Chapter 4     # invalid separator
35:35-Chapter 5      # invalid separator
```

# Hawkeye

Hawkeye is a simple linter for Python. It's a static code analysis tool to catch errors and enforce style rules.

Features:
(✅ - Completed, 🚧 - WIP)
* Unused variables that might indicate a typo or an oversight. ✅
* Incorrect indentation or inconsistent spacing. 🚧
* Trailing whitespace at the end of a line. 🚧
* Lines that are too long according to a style guide. 🚧
* Using deprecated functions or common anti-patterns. 🚧

## Installation

The current way to install hawkeye is from source.

### From source

`git clone https://github.com/philippark/Hawkeye.git`
`cd hawkeye`

## Usage

`python linter.py <file_to_lint.py>`
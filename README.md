# PYLS

Pyls is a python emulator of the unix command [ls](https://man7.org/linux/man-pages/man1/ls.1.html), providing a feature-rich command-line interface to inspect directory contents.

## Installation

Follow these steps to install and set up Pyls:

1. **Clone this repository**

   Clone this repository and navigate into it:
   ```bash
   git clone https://github.com/interseba5/pyls.git
   cd pyls
   ```
2. **Create the metadata file:**

   Create a `structure.json` file inside the `pyls` folder. This file defines the directory structure for Pyls. The file must follow this format:
   ```json
   {
    "name": "<root_name>",
    "size": "<root_dir_size>",
    "time_modified": "<root_last_modification_epoch>",
    "permissions": "<root_permissions>",
    "contents": [
        {
          "name": "<nested_file_name>",
          "size": "<nested_file_size>",
          "time_modified": "<nested_file_last_modification_epoch>",
          "permissions": "<nested_file_permissions>"
        },
        {
          "name": "<nested_directory_name>",
          "size": "<nested_directory_size>",
          "time_modified": "<nested_directory_last_modification_epoch>",
          "permissions": "<nested_directory_permissions>"
          "contents": [
             "<other_nested_nodes>"
           ]
        },
        "<other_nested_nodes>"
      ]
    }
   ```
3. **Install the package**:

   Install the pyls package with `pip`
   ```
   pip install .
   ```
Once installed, the `pyls` command is ready to use.

## Usage
Pyls exposes a command line interface with the following options:

usage: pyls \[-A\] \[-l\] \[-r\] \[-t\] \[--filter {file,dir}\] \[-h\] \[--help\] \[directory\]

optional arguments:
- **-A**: do not ignore entries starting with .
- **-l**: use a long listing format
- **-r**: reverse order while sorting
- **-t**: sort by time, oldest first
- **--filter {file,dir}**: filter the output based on given option. Use 'file' to print only files. Use 'dir' to print only directories
- **-h**: with -l, show human readable size like 1K 234M 2G etc.
- **--help**: display the help message and exit

## Requirements
Pyls requires `Python 3.9` or higher.

## Unit test
This repository includes a comprehensive suite of unit tests to validate all major features. The tests are made using `pytest` and `pytest-mock`.

### How to run tests

1. **Install the development requirements:**
   ```python
   pip install -r requirements-dev.txt
   ```
2. **Execute tests:**
   ```
   pytest
   ```

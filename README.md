[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)
# Generate_TeratermMacro

A Python tool that generates Tera Term macro files (.ttl) from a CSV.

---

## Requirements

- Python **3.13**

---

## How to Use

### 1) Clone and move into the repo
```git bash
git clone https://github.com/<your-user>/Generate_TeratermMacro.git
cd Generate_TeratermMacro
```
### 2) Prepare a CSV

#### Header (5 columns, in this order):

HOST,USERNAME,PASSWORD,INI_FILE,DISPLAY_NAME


- **HOST**: target hostname (e.g., `server1`)
- **USERNAME**: login user (e.g., `root`)
- **PASSWORD**: password (plain text)
- **INI_FILE**: platform key, mapped to a specific Tera Term INI file
- **DISPLAY_NAME**: description / label for the server

#### INI_FILE behavior

```python
INI mapping (used by the tool):

INI_MAP = {
  'Linux': 'LNX_TERATERM.INI',
  'AIX':   'AIX_TERATERM.INI',
}
```

If INI_FILE is Linux → uses LNX_TERATERM.INI

If INI_FILE is AIX → uses AIX_TERATERM.INI


#### DISPLAY_NAME behavior

- When provided, the generated macro filename will be:

  `<USERNAME>@<DISPLAY_NAME>(<HOST>)`.ttl

  and the Tera Term window title will show `<DISPLAY_NAME>(<HOST>)`.

- When empty, the filename will be:

  `<USERNAME>@<HOST>`.ttl

  and the Tera Term window title will show `<HOST>`.

#### Example CSV
```csv
HOST,USERNAME,PASSWORD,INI_FILE,DISPLAY_NAME
server1,root,passw0rd,Linux,WEBserver1
server2,root,passw0rd,AIX,DB01
server3,root,passw0rd,Linux
```

#### Notes on CSV
- The CSV **must** include the header line shown above.
- At least one data row is required. If the CSV only contains the header with no rows, generation will fail.
- In CUI mode, if no macros are generated (due to missing header or empty data), the program will exit with code 1.

### 3) Run (CLI)

From the `current working directory` (where both servers.csv and template.ttl exist):
```cmd
python macro_cui.py
```

- No arguments are required.

- The tool expects servers.csv and template.ttl to be located in the current working directory.

- Generated .ttl files are written to ./output_macros/ under the current working directory.

### 4) Run (GUI)
```cmd
python macro_gui.py
```

- You can choose any CSV and template file, and select any output directory.

- CSV can be provided in two ways:

  - Load from file, or

  - Direct input in the GUI (you can skip preparing a CSV file beforehand).

---
### Files

- macro_common.py — common utilities

- macro_cui.py — CLI interface

- macro_gui.py — GUI interface

- template.ttl — Tera Term macro template

- servers.csv — example input

- ./output_macros/ — output directory for generated .ttl files

---
### Version History

- v1.0 — Initial release

- v1.1 — Bug fixes & enhancements

- v1.1.1 — Added README.md (usage & CSV format)

---
### License

MIT License (see LICENSE)

---


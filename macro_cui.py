# macro_cui.py
from pathlib import Path
from macro_common import generate_and_save_all

TEMPLATE_FILE = 'template.ttl'
CSV_FILE = 'servers.csv'
OUTPUT_DIR = Path('output_macros')

generate_and_save_all(TEMPLATE_FILE, CSV_FILE, OUTPUT_DIR)
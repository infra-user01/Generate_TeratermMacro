# macro_common.py

import csv
from pathlib import Path

INI_MAP = {
  'Linux': 'LNX_TERATERM.INI',
  'AIX': 'AIX_TERATERM.INI'
}

REQUIRED_FIELDS = ['HOST', 'USERNAME', 'PASSWORD', 'INI_FILE', 'DISPLAY_NAME']

def get_ini_file(os_type):
  return INI_MAP.get(os_type, 'UNKNOWN.INI')

def load_template(template_path, encoding='UTF-8'):
  try:
    with open(template_path, 'r', encoding=encoding) as f:
      return f.read()
  except FileNotFoundError:
    print(f"[ERROR] テンプレートファイル '{template_path}' が見つかりません")
    return None
  except Exception as e:
    print(f"[ERROR] テンプレート読み込み中にエラーが発生しました: {e}")
    return None

def load_csv(csv_path, encoding='utf-8'):
  try:
    with open(csv_path, newline='', encoding=encoding) as csvfile:
      return list(csv.DictReader(csvfile))
  except FileNotFoundError:
    print(f"[ERROR] CSVファイル '{csv_path}' が見つかりません")
    return None
  except Exception as e:
    print(f"[ERROR] CSV読み込み中にエラーが発生しました: {e}")
    return None

def _validate_rows(rows):
  if not rows:
    raise ValueError("CSVにデータがありません。ヘッダー行と1行以上のデータを用意してください。")
  keys = rows[0].keys()
  missing = [k for k in REQUIRED_FIELDS if k not in keys]
  if missing:
    raise ValueError("CSVヘッダーに不足があります: " + ", ".join(missing))

def generate_macro(template, row):
  ini_file = get_ini_file(row['INI_FILE'])
  display_name = row.get('DISPLAY_NAME')
  if display_name:
    title = f"{display_name}({row['HOST']})"
  else:
    title = row['HOST']

  return template.format(
    HOST=row['HOST'],
    PORT='22',
    USERNAME=row['USERNAME'],
    PASSWORD=row['PASSWORD'],
    INI_FILENAME=ini_file,
    TITLE=title
  )

def save_macro(output_path, content):
  try:
    with open(output_path, 'w', encoding='utf-8') as f:
      f.write(content)
    return True
  except Exception as e:
    print(f"[ERROR] ファイル保存中にエラーがはっせいしました: {e}")
    return False

def generate_and_save_all(template_path, csv_path, output_dir, log_func=print, csv_encoding='utf-8'):
  template = load_template(template_path)
  if template is None:
    return 0

  rows = load_csv(csv_path, encoding=csv_encoding)   # ★ ここでエンコーディング反映
  if rows is None:
    return 0

  # ★ ヘッダー検証
  try:
    _validate_rows(rows)
  except ValueError as ve:
    log_func(f"[ERROR] {ve}")
    return 0

  Path(output_dir).mkdir(parents=True, exist_ok=True)

  ok = 0
  for row in rows:
    macro_str = generate_macro(template, row)
    display_name = row.get('DISPLAY_NAME')
    if display_name:
      filename = f"{row['USERNAME']}@{display_name}({row['HOST']}).ttl"
    else:
      filename = f"{row['USERNAME']}@{row['HOST']}.ttl"

    output_path = Path(output_dir) / filename

    if save_macro(output_path, macro_str):
      ok += 1
      log_func(f"[OK] {filename} を生成しました")
    else:
      log_func(f"[ERROR] {filename} の保存に失敗しました")

  return ok  # ★ 生成件数を返す
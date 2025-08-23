# macro_cui.py
import sys
from pathlib import Path
from macro_common import generate_and_save_all

TEMPLATE_FILE = 'template.ttl'
CSV_FILE = 'servers.csv'
OUTPUT_DIR = Path('output_macros')

def main():
    def log(msg):
        print(msg)

    count = generate_and_save_all(
        TEMPLATE_FILE,
        CSV_FILE,
        OUTPUT_DIR,
        log_func=log,
        csv_encoding='utf-8'   # 固定
    )

    if count > 0:
        print(f"[INFO] 生成完了: {count} 件")
        sys.exit(0)
    else:
        print("[WARN] 生成されたファイルはありません。CSV未入力/ヘッダー不足/データ0件の可能性があります。")
        sys.exit(1)

if __name__ == "__main__":
    main()
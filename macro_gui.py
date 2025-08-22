import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from macro_common import generate_and_save_all
import tempfile
import os

class MacroGeneratorApp:
    def __init__(self, root):
        self.root = root
        root.title("Tera Term マクロ生成ツール v1.1")
        root.geometry("750x550")

        self.template_path = tk.StringVar()
        self.csv_path = tk.StringVar()
        self.output_dir = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # 実行ボタン
        top_frame = tk.Frame(self.root)
        top_frame.pack(anchor='w', padx=10, pady=(10, 0))
        tk.Button(top_frame, text="▶マクロ生成", command=self.run_generate).pack()

        # テンプレートと出力先は共通
        self.create_file_input("テンプレートファイル:", self.template_path, self.select_template)
        self.create_file_input("出力フォルダ:", self.output_dir, self.select_output_dir)

        # CSV入力方法タブ
        self.tab_control = ttk.Notebook(self.root)
        self.tab_file = tk.Frame(self.tab_control, bg="#e6f2ff")   # 淡い青
        self.tab_text = tk.Frame(self.tab_control, bg="#fff8dc")   # 淡い黄色
        self.tab_control.add(self.tab_file, text="CSVファイルを選択")
        self.tab_control.add(self.tab_text, text="CSVを直接入力")
        self.tab_control.pack(expand=True, fill='both', padx=10, pady=5)

        # CSVファイル選択タブ
        self.create_file_input("CSVファイル:", self.csv_path, self.select_csv, parent=self.tab_file)

        # CSV直接入力タブ
        tk.Label(self.tab_text, text="ここにCSVデータを直接入力してください", bg="#fff8dc").pack(anchor='w', padx=5, pady=5)
        self.csv_text = scrolledtext.ScrolledText(self.tab_text, height=10)
        self.csv_text.pack(fill='both', expand=True, padx=5, pady=5)

        # ログ出力
        tk.Label(self.root, text="ログ出力:").pack(anchor='w', padx=10, pady=(5,0))
        self.log_text = scrolledtext.ScrolledText(self.root, height=12, state='normal')
        self.log_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        # タブ切替イベントで背景色と入力クリア制御
        self.tab_control.bind("<<NotebookTabChanged>>", self.on_tab_change)

        # 初期色設定
        self._update_background_color()

    def create_file_input(self, label_text, variable, command, parent=None):
        """ラベル＋エントリ＋参照ボタン"""
        if parent is None:
            parent = self.root
        frame = tk.Frame(parent)
        frame.pack(fill='x', padx=10, pady=5)

        tk.Label(frame, text=label_text, width=18, anchor='w').pack(side='left')
        entry = tk.Entry(frame, textvariable=variable)
        entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        tk.Button(frame, text="参照", command=command, width=8).pack(side='right')

    # ===== ファイル選択系 =====
    def select_template(self):
        path = filedialog.askopenfilename(filetypes=[("TTL Files", "*.ttl"), ("All Files", "*")])
        if path:
            self.template_path.set(path)

    def select_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if path:
            self.csv_path.set(path)

    def select_output_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.output_dir.set(path)

    # ===== GUI専用: 直接入力CSV → 一時ファイル作成 =====
    def _get_csv_source(self):
        """
        現在のタブに応じてCSV入力ソースを返す。
        タブ0: CSVファイル選択モード → ファイルパスをそのまま返す
        タブ1: 直接入力モード → 一時ファイル作成
        """
        current_tab_index = self.tab_control.index(self.tab_control.select())

        if current_tab_index == 0:  # CSVファイル選択モード
            if not self.csv_path.get():
                raise ValueError("CSVファイルが選択されていません。")
            return self.csv_path.get(), None

        elif current_tab_index == 1:  # 直接入力モード
            csv_content = self.csv_text.get("1.0", tk.END).strip()
            if not csv_content:
                raise ValueError("CSVの内容が入力されていません。")
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding='utf-8')
            tmp_file.write(csv_content)
            tmp_file.close()
            return tmp_file.name, tmp_file.name  # 第二戻り値は削除用パス

    def run_generate(self):
        if not self.template_path.get() or not self.output_dir.get():
            messagebox.showwarning("入力不足", "テンプレートと出力フォルダを指定してください。")
            return

        tmp_path = None
        try:
            csv_source, tmp_path = self._get_csv_source()

            def log(msg):
                self.log_text.insert(tk.END, msg + "\n")
                self.log_text.see(tk.END)

            generate_and_save_all(
                self.template_path.get(),
                csv_source,
                self.output_dir.get(),
                log_func=log
            )
            messagebox.showinfo("完了", "マクロの生成が完了しました！")

        except Exception as e:
            messagebox.showerror("エラー", f"マクロ生成中にエラーが発生しました:\n{e}")
            self.log_text.insert(tk.END, f"[ERROR] {e}\n")
        finally:
            # 一時ファイル削除（直接入力の場合のみ）
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def on_tab_change(self, event):
        # タブ切替時に背景色変更＆入力内容クリアで誤入力防止
        current_tab = self.tab_control.index(self.tab_control.select())

        if current_tab == 0:
            # CSVファイル入力モード → 直接入力欄をクリア
            self.csv_text.delete("1.0", tk.END)
        else:
            # 直接入力モード → CSVファイルパスをクリア
            self.csv_path.set("")

        self._update_background_color()

    def _update_background_color(self):
        # ウィンドウ背景色をタブに合わせて変更
        current_tab = self.tab_control.index(self.tab_control.select())
        if current_tab == 0:
            self.root.configure(bg="#e6f2ff")  # 淡い青
            self.tab_file.configure(bg="#e6f2ff")
            self.tab_text.configure(bg="#fff8dc")  # 直接入力タブは淡い黄色で維持
        else:
            self.root.configure(bg="#fff8dc")  # 淡い黄色
            self.tab_text.configure(bg="#fff8dc")
            self.tab_file.configure(bg="#e6f2ff")  # CSVタブは淡い青で維持


if __name__ == '__main__':
    root = tk.Tk()
    app = MacroGeneratorApp(root)
    root.mainloop()
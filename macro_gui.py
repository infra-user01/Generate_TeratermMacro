# macro_gui.py
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from macro_common import generate_and_save_all

class MacroGeneratorApp:
  def __init__(self, root):
    self.root = root
    root.title("Tera Term マクロ生成ツールv1.0")
    root.geometry("700x500")

    self.template_path = tk.StringVar()
    self.csv_path = tk.StringVar()
    self.output_dir = tk.StringVar()
    self.create_widgets()

  def create_widgets(self):
    top_frame = tk.Frame(self.root)
    top_frame.pack(anchor='w', padx=10, pady=(10, 0))
    tk.Button(top_frame, text="▶マクロ生成", command=self.run_generate).pack()

    self.create_file_input("テンプレートファイル:", self.template_path, self.select_template)
    self.create_file_input("CSVファイル:", self.csv_path, self.select_csv)
    self.create_file_input("出力フォルダ:", self.output_dir, self.select_output_dir)

    tk.Label(self.root, text="ログ出力:").pack(anchor='w', padx=10, pady=(15,0))
    self.log_text = scrolledtext.ScrolledText(self.root, height=12, state='normal')
    self.log_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))

  def create_file_input(self, label_text, variable, command):
    frame = tk.Frame(self.root)
    frame.pack(fill='x', padx=10, pady=5)

    tk.Label(frame, text=label_text, width=18, anchor='w').pack(side='left')
    entry = tk.Entry(frame, textvariable=variable)
    entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
    tk.Button(frame, text="参照", command=command, width=8).pack(side='right')

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

  def run_generate(self):
    if not self.template_path.get() or not self.csv_path.get() or not self.output_dir.get():
      messagebox.showwarning("入力不足", "すべてのファイル/フォルダを選択してください。")
      return
    
    try:
      def log(msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)

      generate_and_save_all(
        self.template_path.get(),
        self.csv_path.get(),
        self.output_dir.get(),
        log_func=log
      )
      messagebox.showinfo("完了", "マクロの生成が完了しました！")
    except Exception as e:
      messagebox.showerror("エラー", f"マクロ生成中にエラーがはっせいしました:\n{e}")
      self.log_text.insert(tk.END, f"[ERROR] {e}\n")

if __name__ == '__main__':
  root = tk.Tk()
  app = MacroGeneratorApp(root)
  root.mainloop()
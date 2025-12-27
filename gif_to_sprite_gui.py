import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import math
import os
import threading

class GifConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GIF 转精灵图工具")
        self.root.geometry("500x350")
        
        # Variables
        self.file_path = tk.StringVar()
        self.horizontal_var = tk.BooleanVar()
        self.status_var = tk.StringVar(value="请选择 GIF 文件")

        # UI Components
        self.create_widgets()

    def create_widgets(self):
        # File Selection Block
        file_frame = tk.LabelFrame(self.root, text="输入文件", padx=10, pady=10)
        file_frame.pack(fill="x", padx=10, pady=5)

        tk.Entry(file_frame, textvariable=self.file_path, state='readonly').pack(side="left", fill="x", expand=True, padx=(0, 5))
        tk.Button(file_frame, text="浏览...", command=self.browse_file).pack(side="right")

        # Options Block
        options_frame = tk.LabelFrame(self.root, text="选项", padx=10, pady=10)
        options_frame.pack(fill="x", padx=10, pady=5)

        tk.Checkbutton(options_frame, text="横向排布 (所有帧在一行)", variable=self.horizontal_var).pack(anchor="w")

        # Action Block
        tk.Button(self.root, text="开始转换", command=self.start_conversion, bg="#4CAF50", fg="black", height=2).pack(fill="x", padx=20, pady=20)

        # Status Block
        tk.Label(self.root, textvariable=self.status_var, wraplength=480).pack(pady=5)

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("GIF Files", "*.gif"), ("All Files", "*.*")])
        if filename:
            self.file_path.set(filename)
            self.status_var.set("已准备就绪")

    def start_conversion(self):
        gif_path = self.file_path.get()
        if not gif_path:
            messagebox.showwarning("提示", "请先选择一个 GIF 文件")
            return

        self.status_var.set("正在转换中...")
        self.root.update()

        # Run in a separate thread to prevent freezing
        thread = threading.Thread(target=self.convert, args=(gif_path, self.horizontal_var.get()))
        thread.start()

    def convert(self, gif_path, horizontal):
        try:
            # Conversion Logic (Embedded for portability)
            try:
                gif = Image.open(gif_path)
            except IOError:
                self.update_status(f"错误: 无法打开文件 {gif_path}", error=True)
                return

            frames = []
            try:
                while True:
                    frames.append(gif.copy())
                    gif.seek(gif.tell() + 1)
            except EOFError:
                pass

            frame_count = len(frames)
            if frame_count == 0:
                self.update_status("错误: GIF 中没有找到帧", error=True)
                return

            frame_width, frame_height = frames[0].size
            
            if horizontal:
                columns = frame_count
            else:
                columns = math.ceil(math.sqrt(frame_count))
            
            rows = math.ceil(frame_count / columns)
            
            sheet_width = columns * frame_width
            sheet_height = rows * frame_height
            
            sprite_sheet = Image.new("RGBA", (sheet_width, sheet_height), (0, 0, 0, 0))
            
            for i, frame in enumerate(frames):
                col = i % columns
                row = i // columns
                x = col * frame_width
                y = row * frame_height
                
                if frame.mode != 'RGBA':
                    frame = frame.convert('RGBA')
                    
                sprite_sheet.paste(frame, (x, y))

            base_name = os.path.splitext(gif_path)[0]
            output_path = f"{base_name}_sheet.png"

            sprite_sheet.save(output_path)
            
            self.update_status(f"成功! 已保存至:\n{output_path}")
            messagebox.showinfo("成功", f"转换完成！\n保存在: {output_path}")

        except Exception as e:
            self.update_status(f"发生错误: {str(e)}", error=True)
            messagebox.showerror("错误", str(e))

    def update_status(self, message, error=False):
        self.status_var.set(message)

if __name__ == "__main__":
    root = tk.Tk()
    app = GifConverterApp(root)
    root.mainloop()

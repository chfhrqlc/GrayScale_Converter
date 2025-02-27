import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PIL import Image
import numpy as np

class TIFFConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TIF Grayscale 변환기")
        self.root.geometry("450x150")

        # Where to import the image(folder unit)
        self.src_label = tk.Label(root, text="불러올 위치:")
        self.src_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.src_entry = tk.Entry(root, width=40)
        self.src_entry.grid(row=0, column=1, padx=5, pady=5)
        self.src_button = tk.Button(root, text="폴더 선택", command=self.select_src_folder)
        self.src_button.grid(row=0, column=2, padx=5, pady=5)

        # Where to save to image(folder unit)
        self.dst_label = tk.Label(root, text="저장할 위치:")
        self.dst_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.dst_entry = tk.Entry(root, width=40)
        self.dst_entry.grid(row=1, column=1, padx=5, pady=5)
        self.dst_button = tk.Button(root, text="폴더 선택", command=self.select_dst_folder)
        self.dst_button.grid(row=1, column=2, padx=5, pady=5)

        self.convert_button = tk.Button(root, text="확인", command=self.convert_images)
        self.convert_button.grid(row=2, column=0, columnspan=3, pady=10)

    def select_src_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.src_entry.delete(0, tk.END)
            self.src_entry.insert(0, folder)

    def select_dst_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dst_entry.delete(0, tk.END)
            self.dst_entry.insert(0, folder)

    def convert_images(self):
        src_folder = self.src_entry.get().strip()
        dst_folder = self.dst_entry.get().strip()

        if not src_folder or not dst_folder:
            messagebox.showerror("오류", "불러올 위치와 저장할 위치를 모두 선택하세요!")
            return

        if not os.path.exists(src_folder):
            messagebox.showerror("오류", "불러올 위치가 존재하지 않습니다.")
            return
        
        os.makedirs(dst_folder, exist_ok=True)

        converted_count = 0
        for filename in os.listdir(src_folder):
            if filename.lower().endswith(".tif"):
                img_path = os.path.abspath(os.path.join(src_folder, filename))  
                save_path = os.path.abspath(os.path.join(dst_folder, filename))  

                try:
                    img = Image.open(img_path)
                    gray = img.convert("L")  # Grayscale conversion
                    gray.save(save_path, format="TIFF")  # Hangul Path Support
                    converted_count += 1
                except Exception as e:
                    print(f"⚠️ 변환 실패: {filename}, 오류: {e}")

        messagebox.showinfo("완료", f"{converted_count}개의 TIFF 이미지를 변환하여 저장했습니다.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TIFFConverterApp(root)
    root.mainloop()

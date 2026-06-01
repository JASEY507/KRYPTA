cat << 'EOF' > ui_components.py
import tkinter as tk
import customtkinter as ctk
import random
from config import Config

class MatrixBackground(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=Config.COLOR_BG_DARK, highlightthickness=0, **kwargs)
        self.font_size = 14
        self.columns = []
        self.active = True
        self.bind("<Configure>", self.reset_matrix)

    def reset_matrix(self, event=None):
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        num_columns = int(self.width / self.font_size) + 1
        self.columns = [random.randint(-100, 0) for _ in range(num_columns)]

    def draw_matrix(self):
        if not self.active: return
        self.delete("all")
        for i, y in enumerate(self.columns):
            char = chr(random.randint(33, 126))
            x = i * self.font_size
            self.create_text(x, y * self.font_size, text=char, fill=Config.COLOR_NEON_RED, font=(Config.FONT_TERMINAL, self.font_size))
            if y * self.font_size > self.height and random.random() > 0.975:
                self.columns[i] = 0
            else:
                self.columns[i] += 1
        self.after(50, self.draw_matrix)

class ConsoleTerminal(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=Config.COLOR_BG_PANEL, border_color=Config.COLOR_NEON_RED, border_width=1, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.text_area = tk.Text(self, bg=Config.COLOR_BG_DARK, fg=Config.COLOR_TEXT_BODY, insertbackground=Config.COLOR_NEON_RED, font=(Config.FONT_TERMINAL, 11), relief="flat", highlightthickness=0, state="disabled")
        self.text_area.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Hatalı olan fg parametreleri, sorun çıkarmayan foreground ile değiştirildi
        self.text_area.tag_config("INFO", foreground=Config.COLOR_NEON_BLUE)
        self.text_area.tag_config("SUCCESS", foreground=Config.COLOR_NEON_GREEN)
        self.text_area.tag_config("ERROR", foreground=Config.COLOR_NEON_RED)

    def write_line(self, message: str, status: str = "INFO"):
        self.text_area.configure(state="normal")
        prefix = f"[+] [{status}] " if status != "ERROR" else "[-] [CRIT] "
        self.text_area.insert("end", f"{prefix} {message}\n", status)
        self.text_area.configure(state="disabled")
        self.text_area.see("end")
EOF

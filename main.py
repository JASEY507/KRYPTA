import os
import threading
import shutil
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from config import Config
from database import DatabaseManager
from crypto_engine import CryptoEngine
from ui_components import MatrixBackground, ConsoleTerminal

class KryptaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(Config.APP_TITLE)
        self.geometry(f"{Config.WIDTH}x{Config.HEIGHT}")
        self.configure(fg_color=Config.COLOR_BG_DARK)
        
        self.db = DatabaseManager()
        self.selected_paths = []
        self.current_lang = "EN" # Varsayılan dil
        
        self.show_auth_screen()

    def show_auth_screen(self):
        self.auth_frame = ctk.CTkFrame(self, fg_color=Config.COLOR_BG_DARK)
        self.auth_frame.pack(fill="both", expand=True)
        
        self.matrix_canvas = MatrixBackground(self.auth_frame)
        self.matrix_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.matrix_canvas.draw_matrix()
        
        # Giriş Paneli
        self.login_panel = ctk.CTkFrame(self.auth_frame, fg_color=Config.COLOR_BG_PANEL, border_color=Config.COLOR_NEON_RED, border_width=2, width=440, height=360)
        self.login_panel.place(relx=0.5, rely=0.5, anchor="center")
        self.login_panel.pack_propagate(False)
        
        # DİL SEÇİM MENÜSÜ (Açılış Ekranında Üstte Yer Alır)
        self.lang_switch = ctk.CTkComboBox(self.login_panel, values=["EN", "TR"], width=70, fg_color=Config.COLOR_BG_DARK, border_color=Config.COLOR_NEON_BLUE, button_color=Config.COLOR_NEON_BLUE, command=self.change_language)
        self.lang_switch.set("EN")
        self.lang_switch.pack(anchor="ne", padx=15, pady=10)
        
        self.lbl_title = ctk.CTkLabel(self.login_panel, text=Config.LANGUAGES[self.current_lang]["auth_title"], font=(Config.FONT_TERMINAL, 15, "bold"), text_color=Config.COLOR_NEON_RED)
        self.lbl_title.pack(pady=15)
        
        self.entry_pin = ctk.CTkEntry(self.login_panel, placeholder_text=Config.LANGUAGES[self.current_lang]["placeholder_master"], show="*", width=320, fg_color=Config.COLOR_BG_DARK, border_color=Config.COLOR_TEXT_MUTED, font=(Config.FONT_INTERFACE, 13))
        self.entry_pin.pack(pady=20)
        
        self.btn_auth = ctk.CTkButton(self.login_panel, text=Config.LANGUAGES[self.current_lang]["btn_enter"], fg_color=Config.COLOR_NEON_RED, text_color="#FFFFFF", font=(Config.FONT_TERMINAL, 13, "bold"), hover_color="#B3002A", command=self.authenticate)
        self.btn_auth.pack(pady=15)
        
        self.lbl_error = ctk.CTkLabel(self.login_panel, text="", font=(Config.FONT_TERMINAL, 11), text_color=Config.COLOR_NEON_RED)
        self.lbl_error.pack(pady=5)

    def change_language(self, choice):
        self.current_lang = choice
        # Giriş ekranı ögelerini gerçek zamanlı güncelle
        self.lbl_title.configure(text=Config.LANGUAGES[choice]["auth_title"])
        self.entry_pin.configure(placeholder_text=Config.LANGUAGES[choice]["placeholder_master"])
        self.btn_auth.configure(text=Config.LANGUAGES[choice]["btn_enter"])

    def authenticate(self):
        password = self.entry_pin.get()
        if len(password) >= 4:
            self.master_password = password
            self.matrix_canvas.active = False
            self.auth_frame.destroy()
            self.build_dashboard()
        else:
            self.lbl_error.configure(text=Config.LANGUAGES[self.current_lang]["err_short"])

    def build_dashboard(self):
        ln = Config.LANGUAGES[self.current_lang]
        
        self.grid_columnconfigure(0, weight=1, minsize=330)
        self.grid_columnconfigure(1, weight=2, minsize=650)
        self.grid_rowconfigure(0, weight=1)
        
        # PANEL 1: Kontrol Paneli (Sol)
        left_panel = ctk.CTkFrame(self, fg_color=Config.COLOR_BG_PANEL, border_color=Config.COLOR_TEXT_MUTED, border_width=1)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        lbl_section = ctk.CTkLabel(left_panel, text=ln["core_engine"], font=(Config.FONT_TERMINAL, 14, "bold"), text_color=Config.COLOR_NEON_BLUE)
        lbl_section.pack(pady=15)
        
        crypto_frame = ctk.CTkFrame(left_panel, fg_color=Config.COLOR_BG_DARK)
        crypto_frame.pack(fill="x", padx=15, pady=10)
        
        lbl_p_info = ctk.CTkLabel(crypto_frame, text=ln["lbl_session"], font=(Config.FONT_INTERFACE, 12), text_color=Config.COLOR_TEXT_BODY)
        lbl_p_info.pack(anchor="w", padx=10, pady=5)
        
        self.entry_crypto_pass = ctk.CTkEntry(crypto_frame, placeholder_text="Cipher Key", show="*", fg_color=Config.COLOR_BG_PANEL, border_color=Config.COLOR_NEON_BLUE)
        self.entry_crypto_pass.pack(fill="x", padx=10, pady=5)
        self.entry_crypto_pass.insert(0, self.master_password)
        self.entry_crypto_pass.bind("<KeyRelease>", self.check_pass_strength)
        
        self.p_strength_bar = ctk.CTkProgressBar(crypto_frame, progress_color=Config.COLOR_NEON_GREEN, fg_color=Config.COLOR_BG_PANEL)
        self.p_strength_bar.pack(fill="x", padx=10, pady=5)
        self.p_strength_bar.set(0.1)
        
        self.lbl_strength_str = ctk.CTkLabel(crypto_frame, text=ln["strength_analyzing"], font=(Config.FONT_TERMINAL, 11), text_color=Config.COLOR_TEXT_MUTED)
        self.lbl_strength_str.pack(anchor="w", padx=10, pady=2)
        
        opt_frame = ctk.CTkFrame(left_panel, fg_color=Config.COLOR_BG_DARK)
        opt_frame.pack(fill="x", padx=15, pady=10)
        
        self.cb_backup = ctk.CTkCheckBox(opt_frame, text=ln["cb_backup"], text_color=Config.COLOR_TEXT_BODY, fg_color=Config.COLOR_NEON_BLUE, hover_color=Config.COLOR_NEON_BLUE)
        self.cb_backup.pack(anchor="w", padx=10, pady=8)
        
        self.cb_shred = ctk.CTkCheckBox(opt_frame, text=ln["cb_shred"], text_color=Config.COLOR_TEXT_BODY, fg_color=Config.COLOR_NEON_RED, hover_color=Config.COLOR_NEON_RED)
        self.cb_shred.pack(anchor="w", padx=10, pady=8)
        
        btn_select = ctk.CTkButton(left_panel, text=ln["btn_select"], fg_color="transparent", border_color=Config.COLOR_NEON_BLUE, border_width=1, hover_color="#1A2332", font=(Config.FONT_TERMINAL, 12, "bold"), command=self.select_files)
        btn_select.pack(fill="x", padx=15, pady=10)
        
        btn_encrypt = ctk.CTkButton(left_panel, text=ln["btn_encrypt"], fg_color=Config.COLOR_NEON_RED, hover_color="#B3002A", font=(Config.FONT_TERMINAL, 13, "bold"), command=lambda: self.run_async(self.process_encryption))
        btn_encrypt.pack(fill="x", padx=15, pady=10)
        
        btn_decrypt = ctk.CTkButton(left_panel, text=ln["btn_decrypt"], fg_color=Config.COLOR_NEON_GREEN, hover_color="#00B347", text_color="#000000", font=(Config.FONT_TERMINAL, 13, "bold"), command=lambda: self.run_async(self.process_decryption))
        btn_decrypt.pack(fill="x", padx=15, pady=10)
        
        # PANEL 2: İzleme Alanı (Sağ)
        right_panel = ctk.CTkFrame(self, fg_color=Config.COLOR_BG_DARK)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.lbl_queue_title = ctk.CTkLabel(right_panel, text=ln["queue_title"], font=(Config.FONT_TERMINAL, 12), text_color=Config.COLOR_TEXT_MUTED)
        self.lbl_queue_title.pack(anchor="w", pady=5)
        
        self.file_listbox = tk.Listbox(right_panel, bg=Config.COLOR_BG_PANEL, fg=Config.COLOR_TEXT_BODY, selectbackground=Config.COLOR_NEON_BLUE, relief="flat", highlightthickness=1, highlightcolor=Config.COLOR_TEXT_MUTED, font=(Config.FONT_INTERFACE, 11))
        self.file_listbox.pack(fill="both", expand=True, pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(right_panel, progress_color=Config.COLOR_NEON_BLUE, fg_color=Config.COLOR_BG_PANEL, height=12)
        self.progress_bar.pack(fill="x", pady=10)
        self.progress_bar.set(0)
        
        self.terminal = ConsoleTerminal(right_panel, height=200)
        self.terminal.pack(fill="x", pady=5)
        
        # Sistem Aktivasyon Logları
        self.terminal.write_line(ln["log_init"], "INFO")
        self.terminal.write_line(ln["log_ready"], "INFO")
        self.db.log_action("SYSTEM_INIT", f"Krypta core booted in {self.current_lang} mode.")
        self.check_pass_strength()

    def check_pass_strength(self, event=None):
        password = self.entry_crypto_pass.get()
        score, label, color = CryptoEngine.analyze_password_strength(password)
        self.p_strength_bar.set(score)
        self.p_strength_bar.configure(progress_color=color)
        self.lbl_strength_str.configure(text=f"{Config.LANGUAGES[self.current_lang]['strength_lbl']}{label}", text_color=color)

    def select_files(self):
        ln = Config.LANGUAGES[self.current_lang]
        paths = filedialog.askopenfilenames(title=ln["select_src"])
        if paths:
            self.selected_paths = list(paths)
            self.file_listbox.delete(0, "end")
            for path in self.selected_paths:
                icon = "📄 " if os.path.isfile(path) else "📁 "
                if path.endswith(".krypta"): icon = "🔒 [SECURE] "
                self.file_listbox.insert("end", f"{icon} {os.path.basename(path)} ({path})")
            self.terminal.write_line(f"{len(self.selected_paths)} {ln['log_queue']}", "INFO")

    def run_async(self, target_function):
        threading.Thread(target=target_function, daemon=True).start()

    def update_progress(self, val):
        self.progress_bar.set(val)
        self.update_idletasks()

    def process_encryption(self):
        ln = Config.LANGUAGES[self.current_lang]
        if not self.selected_paths:
            self.terminal.write_line(ln["err_empty_pool"], "ERROR")
            return
        
        password = self.entry_crypto_pass.get()
        self.terminal.write_line(ln["log_triggered"], "INFO")
        
        for path in self.selected_paths:
            try:
                output_path = path + ".krypta"
                if os.path.isdir(path):
                    self.terminal.write_line(f"{ln['log_zip']}{os.path.basename(path)}", "INFO")
                    file_hash = CryptoEngine.secure_zip_and_encrypt(path, output_path, password, self.update_progress)
                else:
                    if self.cb_backup.get():
                        shutil.copy2(path, path + ".bak")
                        self.terminal.write_line(f"{ln['log_backup']}{os.path.basename(path)}.bak", "INFO")
                        
                    file_hash = CryptoEngine.encrypt_file(path, output_path, password, self.update_progress)
                
                self.db.register_file_hash(output_path, file_hash)
                self.terminal.write_line(f"OK: {os.path.basename(path)} -> SHA-256 Verified.", "SUCCESS")
                
                if self.cb_shred.get():
                    CryptoEngine.secure_shred(path)
                    self.terminal.write_line(ln["log_shred"], "INFO")
                    
            except Exception as e:
                self.terminal.write_line(f"Error [{os.path.basename(path)}]: {str(e)}", "ERROR")
                
        self.update_progress(0)
        self.selected_paths.clear()

    def process_decryption(self):
        ln = Config.LANGUAGES[self.current_lang]
        if not self.selected_paths:
            self.terminal.write_line(ln["err_empty_pool"], "ERROR")
            return
            
        password = self.entry_crypto_pass.get()
        output_dir = filedialog.askdirectory(title=ln["select_dest"])
        if not output_dir: return
        
        for path in self.selected_paths:
            try:
                current_hash = CryptoEngine.calculate_sha256(path)
                registered_hash = self.db.get_registered_hash(path)
                
                if registered_hash and current_hash != registered_hash:
                    self.terminal.write_line(ln["err_manipulated"], "ERROR")
                else:
                    self.terminal.write_line(ln["log_match"], "SUCCESS")
                
                decrypted_file = CryptoEngine.decrypt_file(path, output_dir, password, self.update_progress)
                self.terminal.write_line(f"{ln['log_unlocked']}{os.path.basename(decrypted_file)}", "SUCCESS")
                
            except Exception as e:
                self.terminal.write_line(ln["err_decrypt"], "ERROR")
                
        self.update_progress(0)
        self.selected_paths.clear()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = KryptaApp()
    app.mainloop()

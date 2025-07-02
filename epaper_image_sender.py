import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import serial
import serial.tools.list_ports
from PIL import Image, ImageTk, ImageOps
import threading
import time

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import serial
import serial.tools.list_ports
from PIL import Image, ImageTk, ImageOps
import threading
import time

class EPaperImageSender:
    def __init__(self, root):
        self.root = root
        self.root.title("2.9 inch E-Paper Image Sender")
        self.root.geometry("850x600")
        
        self.setup_styles()
        
        self.EPAPER_WIDTH = 128
        self.EPAPER_HEIGHT = 296
        
        self.serial_connection = None
        self.image_path = None
        self.processed_image = None
        self.processed_image_bw = None
        self.processed_image_4gray = None
        self.current_mode = "bw"  
        
        self.is_processing = False
        self.is_sending = False
        
        self.setup_menu()
        self.setup_ui()
        self.refresh_ports()
    
    def setup_menu(self):
        """Create menu bar with About option"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def show_about(self):
        """Show About dialog with application information"""
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        
        about_window.transient(self.root)
        about_window.grab_set()
        
        main_frame = ttk.Frame(about_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(pady=(0, 15))
        
        app_title = ttk.Label(title_frame, text="E-Paper Image Sender", 
                             font=('Arial', 16, 'bold'))
        app_title.pack()
        
        version_label = ttk.Label(title_frame, text="Version 1.0", 
                                 font=('Arial', 10))
        version_label.pack()
        
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)
        
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        company_label = ttk.Label(info_frame, text="Company:", 
                                 font=('Arial', 10, 'bold'))
        company_label.pack(anchor=tk.W)
        
        company_value = ttk.Label(info_frame, text="Waveshare Electronics", 
                                 font=('Arial', 10))
        company_value.pack(anchor=tk.W, padx=(20, 0))
        
        dev_label = ttk.Label(info_frame, text="Developer:", 
                             font=('Arial', 10, 'bold'))
        dev_label.pack(anchor=tk.W, pady=(10, 0))
        
        dev_value = ttk.Label(info_frame, text="Kalp_D", 
                             font=('Arial', 10))
        dev_value.pack(anchor=tk.W, padx=(20, 0))
        
        desc_label = ttk.Label(info_frame, text="Description:", 
                              font=('Arial', 10, 'bold'))
        desc_label.pack(anchor=tk.W, pady=(10, 0))
        
        desc_value = ttk.Label(info_frame, 
                              text="A GUI application for sending images to\n2.9 inch E-Paper displays via serial communication.\nSupports both B&W and 4-level grayscale modes.", 
                              font=('Arial', 10),
                              justify=tk.LEFT)
        desc_value.pack(anchor=tk.W, padx=(20, 0))
        
        copyright_label = ttk.Label(info_frame, text="© 2024 Waveshare Electronics", 
                                   font=('Arial', 9),
                                   foreground='gray')
        copyright_label.pack(anchor=tk.W, pady=(15, 0))
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(15, 0))
        
        close_btn = ttk.Button(button_frame, text="Close", 
                              command=about_window.destroy)
        close_btn.pack()
        
        close_btn.focus()
        
        about_window.bind('<Escape>', lambda e: about_window.destroy())
        
        about_window.update_idletasks()
        x = (about_window.winfo_screenwidth() // 2) - (about_window.winfo_width() // 2)
        y = (about_window.winfo_screenheight() // 2) - (about_window.winfo_height() // 2)
        about_window.geometry(f"+{x}+{y}")
        
    def setup_styles(self):
        
        self.style = ttk.Style()
        
        
        self.style.theme_use('clam')
        
        
        self.style.configure(
            "Custom.Horizontal.TProgressbar",
            background='#4CAF50',
            troughcolor='#E0E0E0',
            borderwidth=1,
            lightcolor='#4CAF50',
            darkcolor='#388E3C',
            relief='flat',
            thickness=20
        )
        
        
        self.style.configure(
            "Determinate.Horizontal.TProgressbar",
            background='#2196F3',
            troughcolor='#E3F2FD',
            borderwidth=1,
            lightcolor='#2196F3',
            darkcolor='#1976D2',
            relief='flat',
            thickness=20
        )
        
        
        self.style.configure(
            "Sending.Horizontal.TProgressbar",
            background='#FF9800',
            troughcolor='#FFF3E0',
            borderwidth=1,
            lightcolor='#FF9800',
            darkcolor='#F57C00',
            relief='flat',
            thickness=20
        )
        
    def setup_ui(self):
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        
        serial_frame = ttk.LabelFrame(main_frame, text="Serial Connection", padding="10")
        serial_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(serial_frame, text="Port:").grid(row=0, column=0, sticky=tk.W)
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(serial_frame, textvariable=self.port_var, width=15)
        self.port_combo.grid(row=0, column=1, padx=(5, 10))
        
        ttk.Button(serial_frame, text="Refresh", command=self.refresh_ports).grid(row=0, column=2, padx=(0, 10))
        
        ttk.Label(serial_frame, text="Baud Rate:").grid(row=0, column=3, sticky=tk.W)
        self.baud_var = tk.StringVar(value="115200")
        baud_combo = ttk.Combobox(serial_frame, textvariable=self.baud_var, values=["9600", "115200"], width=10)
        baud_combo.grid(row=0, column=4, padx=(5, 10))
        
        self.connect_btn = ttk.Button(serial_frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=5)
        
        self.status_label = ttk.Label(serial_frame, text="Disconnected", foreground="red")
        self.status_label.grid(row=1, column=0, columnspan=6, pady=(5, 0))
        
        
        mode_frame = ttk.LabelFrame(main_frame, text="Processing Options", padding="10")
        mode_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        mode_options_frame = ttk.Frame(mode_frame)
        mode_options_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(mode_options_frame, text="Mode:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.mode_var = tk.StringVar(value="bw")
        ttk.Radiobutton(mode_options_frame, text="Black & White", variable=self.mode_var, value="bw").grid(row=0, column=1, padx=(0, 20))
        ttk.Radiobutton(mode_options_frame, text="4-Level Grayscale", variable=self.mode_var, value="4gray").grid(row=0, column=2)
        
        color_options_frame = ttk.Frame(mode_frame)
        color_options_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Label(color_options_frame, text="Colors:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.invert_var = tk.BooleanVar(value=False)
        self.invert_checkbox = ttk.Checkbutton(
            color_options_frame, 
            text="Invert Colors", 
            variable=self.invert_var,
            command=self.on_invert_changed
        )
        self.invert_checkbox.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        
        self.invert_info = ttk.Label(
            color_options_frame, 
            text="(Makes white→black, black→white)", 
            font=('Arial', 8), 
            foreground='gray'
        )
        self.invert_info.grid(row=0, column=2, sticky=tk.W)
        
        
        image_frame = ttk.LabelFrame(main_frame, text="Image Selection", padding="10")
        image_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(image_frame, text="Browse Image", command=self.browse_image).grid(row=0, column=0, padx=(0, 10))
        self.image_path_label = ttk.Label(image_frame, text="No image selected")
        self.image_path_label.grid(row=0, column=1, sticky=tk.W)
        
        
        preview_frame = ttk.LabelFrame(main_frame, text="Image Preview", padding="10")
        preview_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        self.preview_label = ttk.Label(preview_frame, text="No image loaded")
        self.preview_label.pack()
        
        
        controls_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        controls_frame.grid(row=3, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        self.process_btn = ttk.Button(controls_frame, text="Process Image", command=self.process_image_threaded)
        self.process_btn.pack(pady=(0, 10), fill=tk.X)
        
        self.send_btn = ttk.Button(controls_frame, text="Send to E-Paper", command=self.send_image_threaded)
        self.send_btn.pack(pady=(0, 10), fill=tk.X)
        
        self.clear_btn = ttk.Button(controls_frame, text="Clear Display", command=self.clear_display)
        self.clear_btn.pack(fill=tk.X)
        
        
        progress_section = ttk.Frame(controls_frame)
        progress_section.pack(pady=(15, 0), fill=tk.X)
        
        
        self.progress_label = ttk.Label(progress_section, text="", font=('Arial', 9, 'bold'))
        self.progress_label.pack(pady=(0, 5))
        
        
        self.progress = ttk.Progressbar(
            progress_section, 
            mode='indeterminate',
            style="Custom.Horizontal.TProgressbar",
            length=200
        )
        self.progress.pack(fill=tk.X, pady=(0, 5))
        
        
        self.progress_detailed = ttk.Progressbar(
            progress_section,
            mode='determinate',
            style="Determinate.Horizontal.TProgressbar",
            length=200
        )
        self.progress_detailed.pack(fill=tk.X, pady=(0, 5))
        

        self.progress_percent = ttk.Label(progress_section, text="", font=('Arial', 8))
        self.progress_percent.pack()
        

        self.transfer_progress = ttk.Progressbar(
            progress_section,
            mode='determinate',
            style="Sending.Horizontal.TProgressbar",
            length=200
        )
        self.transfer_progress.pack(fill=tk.X, pady=(5, 0))
        

        self.transfer_stats = ttk.Label(progress_section, text="", font=('Arial', 8))
        self.transfer_stats.pack()
        

        self.status_indicator = tk.Canvas(progress_section, width=20, height=20, highlightthickness=0)
        self.status_indicator.pack(pady=(5, 0))
        self.status_dot = self.status_indicator.create_oval(6, 6, 14, 14, fill='gray', outline='darkgray')
        

        self.progress_detailed.pack_forget()
        self.progress_percent.pack_forget()
        self.transfer_progress.pack_forget()
        self.transfer_stats.pack_forget()
        

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
    def on_invert_changed(self):
        """Handle invert checkbox change - reprocess image if already processed"""
        if self.processed_image and self.image_path:
            self.process_image_threaded()
        
    def update_progress(self, show=True, text="", mode="indeterminate", value=0):
                                                                 
        if show:

            self.status_indicator.itemconfig(self.status_dot, fill='#4CAF50', outline='#388E3C')
            

            self.progress_label.config(text=text, foreground='#1976D2')
            
            if mode == "indeterminate":

                self.progress.pack(fill=tk.X, pady=(0, 5))
                self.progress_detailed.pack_forget()
                self.progress_percent.pack_forget()
                self.transfer_progress.pack_forget()
                self.transfer_stats.pack_forget()
                self.progress.start(10)
                
            elif mode == "determinate":

                self.progress.stop()
                self.progress.pack_forget()
                self.progress_detailed.pack(fill=tk.X, pady=(0, 5))
                self.progress_percent.pack()
                self.transfer_progress.pack_forget()
                self.transfer_stats.pack_forget()
                

                self.progress_detailed['value'] = value
                self.progress_percent.config(text=f"{value:.1f}%")
                
            elif mode == "sending":

                self.progress.stop()
                self.progress.pack_forget()
                self.progress_detailed.pack_forget()
                self.progress_percent.pack_forget()
                self.transfer_progress.pack(fill=tk.X, pady=(5, 0))
                self.transfer_stats.pack()
                

                self.transfer_progress['value'] = value
                
        else:

            self.progress.stop()
            self.progress.pack_forget()
            self.progress_detailed.pack_forget()
            self.progress_percent.pack_forget()
            self.transfer_progress.pack_forget()
            self.transfer_stats.pack_forget()
            self.progress_label.config(text="", foreground='black')
            

            self.status_indicator.itemconfig(self.status_dot, fill='gray', outline='darkgray')
            
        self.root.update()
        
    def update_detailed_progress(self, value, text=""):
                                              
        self.progress_detailed['value'] = value
        self.progress_percent.config(text=f"{value:.1f}%")
        if text:
            self.progress_label.config(text=text)
        self.root.update()
        
    def update_transfer_progress(self, value, bytes_sent, total_bytes, speed_kbps=0):
                                                                  
        self.transfer_progress['value'] = value
        stats_text = f"{bytes_sent:,} / {total_bytes:,} bytes"
        if speed_kbps > 0:
            stats_text += f" ({speed_kbps:.1f} KB/s)"
        self.transfer_stats.config(text=stats_text)
        self.root.update()
        
    def disable_buttons(self):
                                               
        self.process_btn.config(state='disabled')
        self.send_btn.config(state='disabled')
        self.clear_btn.config(state='disabled')
        
    def enable_buttons(self):
                                             
        self.process_btn.config(state='normal')
        self.send_btn.config(state='normal')
        self.clear_btn.config(state='normal')
        
    def refresh_ports(self):
                                            
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combo['values'] = ports
        if ports:
            self.port_combo.set(ports[0])
        
    def toggle_connection(self):
                                                    
        if self.serial_connection is None:
            try:
                port = self.port_var.get()
                baud = int(self.baud_var.get())
                self.serial_connection = serial.Serial(port, baud, timeout=1)
                time.sleep(2)
                
                self.connect_btn.config(text="Disconnect")
                self.status_label.config(text="Connected", foreground="green")
                
            except Exception as e:
                messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
        else:
            self.serial_connection.close()
            self.serial_connection = None
            self.connect_btn.config(text="Connect")
            self.status_label.config(text="Disconnected", foreground="red")
            
    def browse_image(self):
                                             
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.image_path = file_path
            self.image_path_label.config(text=f"Selected: {file_path.split('/')[-1]}")
            
    def process_image_threaded(self):
                                                
        if self.is_processing:
            return
            
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first")
            return
            
        self.is_processing = True
        self.disable_buttons()
        
        invert_text = " (inverted)" if self.invert_var.get() else ""
        self.update_progress(True, f"🔄 Processing image{invert_text}...", "indeterminate")
        
        def process_thread():
            try:
                self.process_image()
            finally:
                self.is_processing = False
                self.enable_buttons()
                self.update_progress(False)
                
        threading.Thread(target=process_thread, daemon=True).start()
            
    def process_image(self):
                                                            
        try:

            self.update_progress(True, "📂 Loading image...", "determinate", 10)
            img = Image.open(self.image_path)
            

            self.update_detailed_progress(30, "🎨 Converting to grayscale...")
            img = img.convert('L')
            time.sleep(0.2)
            

            self.update_detailed_progress(50, "📏 Resizing image...")
            img = img.resize((self.EPAPER_WIDTH, self.EPAPER_HEIGHT), Image.Resampling.LANCZOS)
            time.sleep(0.2)
            
            if self.invert_var.get():
                self.update_detailed_progress(60, "🔄 Inverting colors...")
                img = ImageOps.invert(img)
                time.sleep(0.2)
            
            mode = self.mode_var.get()
            
            if mode == "bw":

                progress_text = "⚫ Converting to B&W..."
                if self.invert_var.get():
                    progress_text += " (inverted)"
                self.update_detailed_progress(75, progress_text)
                img_processed = img.point(lambda x: 0 if x < 128 else 255, '1')
                self.processed_image_bw = img_processed
                self.processed_image = img_processed
                self.current_mode = "bw"
                
            else:

                progress_text = "🔘 Converting to 4-level grayscale..."
                if self.invert_var.get():
                    progress_text += " (inverted)"
                self.update_detailed_progress(75, progress_text)
                
                def quantize_4gray(x):
                    if x < 64:
                        return 0
                    elif x < 128:
                        return 85
                    elif x < 192:
                        return 170
                    else:
                        return 255
                
                img_processed = img.point(quantize_4gray, 'L')
                self.processed_image_4gray = img_processed
                self.processed_image = img_processed
                self.current_mode = "4gray"
            

            self.update_detailed_progress(90, "🖼️ Creating preview...")
            preview_img = img_processed.resize((128//2, 296//2), Image.Resampling.NEAREST)
            preview_photo = ImageTk.PhotoImage(preview_img)
            time.sleep(0.2)
            

            success_text = "✅ Processing complete!"
            if self.invert_var.get():
                success_text += " (Colors inverted)"
            self.update_detailed_progress(100, success_text)
            self.root.after(0, lambda: self.update_preview(preview_photo))
            time.sleep(0.5)
            
        except Exception as e:
            messagebox.showerror("Processing Error", f"Failed to process image: {str(e)}")
            
    def update_preview(self, preview_photo):
                                                 
        self.preview_label.config(image=preview_photo, text="")
        self.preview_label.image = preview_photo
            
    def image_to_hex_bw(self, img):
                                                                       

        pixels = list(img.getdata())
        total_bytes = (self.EPAPER_WIDTH * self.EPAPER_HEIGHT) // 8
        

        hex_data = []
        byte_count = 0
        
        for y in range(self.EPAPER_HEIGHT):
            for x in range(0, self.EPAPER_WIDTH, 8):
                byte_val = 0
                for bit in range(8):
                    if x + bit < self.EPAPER_WIDTH:
                        pixel_index = y * self.EPAPER_WIDTH + x + bit
                        if pixel_index < len(pixels):

                            if pixels[pixel_index] == 255:
                                byte_val |= (1 << (7 - bit))
                hex_data.append(f"0x{byte_val:02X}")
                byte_count += 1
                

                if byte_count % 100 == 0:
                    progress = (byte_count / total_bytes) * 100
                    self.update_detailed_progress(progress, f"📦 Converting data... {byte_count}/{total_bytes}")
                
        return ",".join(hex_data)
    
    def image_to_hex_4gray(self, img):
                                                                           

        pixels = list(img.getdata())
        total_bytes = (self.EPAPER_WIDTH * self.EPAPER_HEIGHT) // 4
        

        def gray_to_2bit(gray_val):
            if gray_val == 0:
                return 0b00
            elif gray_val == 85:
                return 0b01
            elif gray_val == 170:
                return 0b10
            else:
                return 0b11
        

        hex_data = []
        byte_count = 0
        
        for y in range(self.EPAPER_HEIGHT):
            for x in range(0, self.EPAPER_WIDTH, 4):
                byte_val = 0
                for pixel in range(4):
                    if x + pixel < self.EPAPER_WIDTH:
                        pixel_index = y * self.EPAPER_WIDTH + x + pixel
                        if pixel_index < len(pixels):
                            gray_2bit = gray_to_2bit(pixels[pixel_index])
                            byte_val |= (gray_2bit << (6 - pixel * 2))
                hex_data.append(f"0x{byte_val:02X}")
                byte_count += 1
                

                if byte_count % 100 == 0:
                    progress = (byte_count / total_bytes) * 100
                    self.update_detailed_progress(progress, f"📦 Converting data... {byte_count}/{total_bytes}")
                
        return ",".join(hex_data)
        
    def send_image_threaded(self):
                                             
        if self.is_sending:
            return
            
        if not self.serial_connection:
            messagebox.showerror("Error", "Please connect to serial port first")
            return
            
        if not self.processed_image:
            messagebox.showerror("Error", "Please process an image first")
            return
            
        self.is_sending = True
        self.disable_buttons()
        
        send_text = "📡 Preparing to send image..."
        if self.invert_var.get():
            send_text += " (inverted)"
        self.update_progress(True, send_text, "determinate", 0)
        
        def send_thread():
            try:
                self.send_image()
            finally:
                self.is_sending = False
                self.enable_buttons()
                self.update_progress(False)
                
        threading.Thread(target=send_thread, daemon=True).start()
        
    def send_image(self):
                                                                                     
        try:

            convert_text = "🔄 Converting image to hex data..."
            if self.invert_var.get():
                convert_text += " (inverted)"
            self.update_detailed_progress(5, convert_text)
            

            if self.current_mode == "bw":
                hex_data = self.image_to_hex_bw(self.processed_image)
                command = f"START_IMAGE,{hex_data},END_IMAGE"
            else:
                hex_data = self.image_to_hex_4gray(self.processed_image)
                command = f"START_GRAY,{hex_data},END_GRAY"
            

            self.update_detailed_progress(10, "📦 Preparing data for transmission...")
            command_bytes = command.encode('utf-8')
            total_bytes = len(command_bytes)
            

            transmit_text = "📤 Transmitting data to E-Paper..."
            if self.invert_var.get():
                transmit_text += " (inverted image)"
            self.update_progress(True, transmit_text, "sending", 0)
            

            chunk_size = 1024
            bytes_sent = 0
            start_time = time.time()
            

            self.serial_connection.reset_input_buffer()
            self.serial_connection.reset_output_buffer()
            

            for i in range(0, len(command_bytes), chunk_size):
                chunk = command_bytes[i:i + chunk_size]
                self.serial_connection.write(chunk)
                bytes_sent += len(chunk)
                

                progress = (bytes_sent / total_bytes) * 100
                elapsed_time = time.time() - start_time
                if elapsed_time > 0:
                    speed_kbps = (bytes_sent / 1024) / elapsed_time
                else:
                    speed_kbps = 0
                

                self.update_transfer_progress(progress, bytes_sent, total_bytes, speed_kbps)
                

                time.sleep(0.01)
            

            self.update_progress(True, "⏳ Waiting for ESP32 response...", "determinate", 80)
            
            response = ""
            timeout = 45
            start_time = time.time()
            last_update = time.time()
            
            while time.time() - start_time < timeout:
                if self.serial_connection.in_waiting:
                    try:
                        new_data = self.serial_connection.read(self.serial_connection.in_waiting).decode('utf-8', errors='ignore')
                        response += new_data
                        

                        if "DISPLAY_SUCCESS" in response:
                            success_text = "✅ Image displayed successfully!"
                            if self.invert_var.get():
                                success_text += " (Inverted colors)"
                            self.update_detailed_progress(100, success_text)
                            time.sleep(0.5)
                            return
                        elif "DISPLAY_ERROR" in response:
                            messagebox.showerror("Display Error", "ESP32 reported an error while displaying the image")
                            return
                            
                    except UnicodeDecodeError:

                        pass
                

                elapsed = time.time() - start_time
                wait_progress = 80 + (elapsed / timeout) * 19
                

                if time.time() - last_update >= 1.0:
                    self.update_detailed_progress(
                        min(wait_progress, 99), 
                        f"⏳ Waiting for response... ({int(elapsed)}s/{timeout}s)"
                    )
                    last_update = time.time()
                
                time.sleep(0.1)
            

            messagebox.showwarning("Timeout", "Timeout waiting for ESP32 response. The image may have been sent successfully.")
                
        except Exception as e:
            error_msg = f"Failed to send image: {str(e)}"
            messagebox.showerror("Send Error", error_msg)
            
    def clear_display(self):
                                       
        if not self.serial_connection:
            messagebox.showerror("Error", "Please connect to serial port first")
            return
            
        try:
            self.update_progress(True, "🧹 Clearing display...", "indeterminate")
            self.serial_connection.write(b"CLEAR\n")
            

            response = ""
            timeout = 15
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                if self.serial_connection.in_waiting:
                    try:
                        new_data = self.serial_connection.read(self.serial_connection.in_waiting).decode('utf-8', errors='ignore')
                        response += new_data
                        
                        if "CLEAR_SUCCESS" in response:
                            break
                        elif "CLEAR_ERROR" in response:
                            break
                            
                    except UnicodeDecodeError:
                        pass
                        
                time.sleep(0.1)
                
            time.sleep(1)
            self.update_progress(False)
            
        except Exception as e:
            self.update_progress(False)

if __name__ == "__main__":
    root = tk.Tk()
    app = EPaperImageSender(root)
    root.mainloop()

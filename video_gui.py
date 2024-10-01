import tkinter as tk
from tkinter import filedialog, messagebox


class VideoCompressorGUI:
    def __init__(self, root, handle_compression, handle_audio_conversion):
        self.root = root
        self.root.title("Video Utility Tool")
        self.root.geometry("500x500")
        
        self.file_path = None

        # Title Label
        self.title_label = tk.Label(root, text="Video Utility Tool", font=("Arial", 16))
        self.title_label.pack(pady=10)

        # File Selection
        self.file_label = tk.Label(root, text="Select a video file:")
        self.file_label.pack(pady=5)

        self.select_button = tk.Button(root, text="Select File", command=self.select_file)
        self.select_button.pack(pady=5)

        # Compression Button
        self.compress_button = tk.Button(root, text="Compress Video", command=lambda: handle_compression(self.file_path), state=tk.DISABLED)
        self.compress_button.pack(pady=10)

        # Audio Extraction Parameters
        self.audio_settings_label = tk.Label(root, text="Audio Extraction Settings:", font=("Arial", 12))
        self.audio_settings_label.pack(pady=10)

        # Bitrate Selection
        self.bitrate_label = tk.Label(root, text="Bitrate (Quality):")
        self.bitrate_label.pack()
        self.bitrate_options = ["Best (320 kbps)", "Normal (128 kbps)", "Lowest (64 kbps)"]
        self.bitrate_var = tk.StringVar(root)
        self.bitrate_var.set(self.bitrate_options[1])  # Default to "Normal"
        self.bitrate_menu = tk.OptionMenu(root, self.bitrate_var, *self.bitrate_options)
        self.bitrate_menu.pack()

        # Channels Selection
        self.channels_label = tk.Label(root, text="Channels:")
        self.channels_label.pack()
        self.channels_options = ["Stereo (2 channels)", "Mono (1 channel)"]
        self.channels_var = tk.StringVar(root)
        self.channels_var.set(self.channels_options[0])  # Default to "Stereo"
        self.channels_menu = tk.OptionMenu(root, self.channels_var, *self.channels_options)
        self.channels_menu.pack()

        # Sample Rate Selection
        self.sample_rate_label = tk.Label(root, text="Sample Rate:")
        self.sample_rate_label.pack()
        self.sample_rate_options = ["Best (44100 Hz)", "Normal (22050 Hz)", "Lowest (11025 Hz)"]
        self.sample_rate_var = tk.StringVar(root)
        self.sample_rate_var.set(self.sample_rate_options[0])  # Default to "Best"
        self.sample_rate_menu = tk.OptionMenu(root, self.sample_rate_var, *self.sample_rate_options)
        self.sample_rate_menu.pack()

        # Convert to Audio Button
        self.convert_button = tk.Button(root, text="Convert to Audio", 
                                        command=lambda: handle_audio_conversion(
                                            self.file_path,
                                            self.bitrate_var.get(),
                                            self.channels_var.get(),
                                            self.sample_rate_var.get()
                                        ),
                                        state=tk.DISABLED)
        self.convert_button.pack(pady=20)

        # Explanation for Settings
        self.explanation_label = tk.Label(root, text="Settings Guide:\n- Bitrate: Higher bitrate = Better quality but larger file size.\n"
                                                     "- Channels: Stereo has better spatial audio quality; Mono is smaller.\n"
                                                     "- Sample Rate: Higher rate = Better quality but larger file size.", 
                                          font=("Arial", 10), justify=tk.LEFT)
        self.explanation_label.pack(pady=10)

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mkv *.avi *.mov")])
        if self.file_path:
            self.file_label.config(text=f"Selected: {self.file_path}")
            self.compress_button.config(state=tk.NORMAL)
            self.convert_button.config(state=tk.NORMAL)

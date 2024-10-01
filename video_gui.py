import tkinter as tk
from tkinter import filedialog, messagebox


class VideoCompressorGUI:
    def __init__(self, root, handle_compression, handle_audio_conversion):
        self.root = root
        self.root.title("Video Utility Tool")
        self.root.geometry("500x450")
        
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

        self.bitrate_label = tk.Label(root, text="Bitrate (kbps):")
        self.bitrate_label.pack()
        self.bitrate_entry = tk.Entry(root)
        self.bitrate_entry.insert(0, "128")  # Default bitrate value
        self.bitrate_entry.pack()

        self.channels_label = tk.Label(root, text="Channels (1 for Mono, 2 for Stereo):")
        self.channels_label.pack()
        self.channels_entry = tk.Entry(root)
        self.channels_entry.insert(0, "2")  # Default channels value (Stereo)
        self.channels_entry.pack()

        self.sample_rate_label = tk.Label(root, text="Sample Rate (Hz):")
        self.sample_rate_label.pack()
        self.sample_rate_entry = tk.Entry(root)
        self.sample_rate_entry.insert(0, "44100")  # Default sample rate value
        self.sample_rate_entry.pack()

        # Convert to Audio Button
        self.convert_button = tk.Button(root, text="Convert to Audio", 
                                        command=lambda: handle_audio_conversion(
                                            self.file_path,
                                            self.bitrate_entry.get(),
                                            self.channels_entry.get(),
                                            self.sample_rate_entry.get()
                                        ),
                                        state=tk.DISABLED)
        self.convert_button.pack(pady=20)

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mkv *.avi *.mov")])
        if self.file_path:
            self.file_label.config(text=f"Selected: {self.file_path}")
            self.compress_button.config(state=tk.NORMAL)
            self.convert_button.config(state=tk.NORMAL)

import tkinter as tk
from tkinter import filedialog, messagebox

class VideoUtilityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Utility Tool")
        self.root.geometry("500x500")
        self.handle_compression = None
        self.handle_audio_conversion = None
        self.handle_audio_to_text = None
        self.file_path = None
        self.create_main_menu()

    def create_main_menu(self):
        # Clear existing UI elements
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title Label
        self.title_label = tk.Label(self.root, text="What do you want to do?", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # Option Buttons
        self.compress_video_button = tk.Button(self.root, text="Compress Video", command=self.create_compress_video_screen)
        self.compress_video_button.pack(pady=10)

        self.video_to_audio_button = tk.Button(self.root, text="Convert Video to Audio", command=self.create_video_to_audio_screen)
        self.video_to_audio_button.pack(pady=10)

        self.audio_to_transcript_button = tk.Button(self.root, text="Convert Audio to Transcript", command=self.create_audio_to_transcript_screen)
        self.audio_to_transcript_button.pack(pady=10)

    def create_compress_video_screen(self):
        # Clear existing UI elements
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title Label
        self.title_label = tk.Label(self.root, text="Compress Video", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # File Selection
        self.file_label = tk.Label(self.root, text="Select a video file:")
        self.file_label.pack(pady=5)

        self.select_button = tk.Button(self.root, text="Select File", command=self.select_file_compress)
        self.select_button.pack(pady=5)

        # Compress Button
        self.compress_button = tk.Button(self.root, text="Compress Video", command=lambda: self.handle_compression(self.file_path), state=tk.DISABLED)
        self.compress_button.pack(pady=10)

        # Back Button
        self.back_button = tk.Button(self.root, text="Back", command=self.create_main_menu)
        self.back_button.pack(pady=20)

    def create_video_to_audio_screen(self):
        # Clear existing UI elements
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title Label
        self.title_label = tk.Label(self.root, text="Convert Video to Audio", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # File Selection
        self.file_label = tk.Label(self.root, text="Select a video file:")
        self.file_label.pack(pady=5)

        self.select_button = tk.Button(self.root, text="Select File", command=self.select_file_audio)
        self.select_button.pack(pady=5)

        # Audio Extraction Parameters
        self.audio_settings_label = tk.Label(self.root, text="Audio Extraction Settings:", font=("Arial", 12))
        self.audio_settings_label.pack(pady=10)

        # Bitrate Selection
        self.bitrate_label = tk.Label(self.root, text="Bitrate (Quality):")
        self.bitrate_label.pack()
        self.bitrate_options = ["Best (320 kbps)", "Normal (128 kbps)", "Lowest (64 kbps)"]
        self.bitrate_var = tk.StringVar(self.root)
        self.bitrate_var.set(self.bitrate_options[1])  # Default to "Normal"
        self.bitrate_menu = tk.OptionMenu(self.root, self.bitrate_var, *self.bitrate_options)
        self.bitrate_menu.pack()

        # Channels Selection
        self.channels_label = tk.Label(self.root, text="Channels:")
        self.channels_label.pack()
        self.channels_options = ["Stereo (2 channels)", "Mono (1 channel)"]
        self.channels_var = tk.StringVar(self.root)
        self.channels_var.set(self.channels_options[0])  # Default to "Stereo"
        self.channels_menu = tk.OptionMenu(self.root, self.channels_var, *self.channels_options)
        self.channels_menu.pack()

        # Sample Rate Selection
        self.sample_rate_label = tk.Label(self.root, text="Sample Rate:")
        self.sample_rate_label.pack()
        self.sample_rate_options = ["Best (44100 Hz)", "Normal (22050 Hz)", "Lowest (11025 Hz)"]
        self.sample_rate_var = tk.StringVar(self.root)
        self.sample_rate_var.set(self.sample_rate_options[0])  # Default to "Best"
        self.sample_rate_menu = tk.OptionMenu(self.root, self.sample_rate_var, *self.sample_rate_options)
        self.sample_rate_menu.pack()

        # Convert to Audio Button
        self.convert_button = tk.Button(self.root, text="Convert to Audio", 
                                        command=lambda: self.handle_audio_conversion(
                                            self.file_path,
                                            self.bitrate_var.get(),
                                            self.channels_var.get(),
                                            self.sample_rate_var.get()
                                        ),
                                        state=tk.DISABLED)
        self.convert_button.pack(pady=20)

        # Back Button
        self.back_button = tk.Button(self.root, text="Back", command=self.create_main_menu)
        self.back_button.pack(pady=20)

    def create_audio_to_transcript_screen(self):
        # Clear existing UI elements
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title Label
        self.title_label = tk.Label(self.root, text="Convert Audio to Transcript", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # File Selection
        self.file_label = tk.Label(self.root, text="Select an audio file:")
        self.file_label.pack(pady=5)

        self.select_button = tk.Button(self.root, text="Select File", command=self.select_file_transcript)
        self.select_button.pack(pady=5)

        # Convert to Transcript Button
        self.transcript_button = tk.Button(self.root, text="Convert to Transcript", command=lambda: self.handle_audio_to_text(self.file_path), state=tk.DISABLED)
        self.transcript_button.pack(pady=20)

        # Back Button
        self.back_button = tk.Button(self.root, text="Back", command=self.create_main_menu)
        self.back_button.pack(pady=20)

    def select_file_compress(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mkv *.avi *.mov")])
        if self.file_path:
            self.file_label.config(text=f"Selected: {self.file_path}")
            self.compress_button.config(state=tk.NORMAL)

    def select_file_audio(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mkv *.avi *.mov")])
        if self.file_path:
            self.file_label.config(text=f"Selected: {self.file_path}")
            self.convert_button.config(state=tk.NORMAL)

    def select_file_transcript(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav")])
        if self.file_path:
            self.file_label.config(text=f"Selected: {self.file_path}")
            self.transcript_button.config(state=tk.NORMAL)

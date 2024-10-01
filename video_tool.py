import os
import ffmpeg
from tkinter import messagebox, filedialog
import tkinter as tk
from video_gui import VideoCompressorGUI


def handle_compression(file_path):
    if not file_path:
        messagebox.showerror("Error", "No file selected!")
        return

    # Choose output file path
    output_path = filedialog.asksaveasfilename(defaultextension=".mp4",
                                               filetypes=[("MP4 files", "*.mp4")],
                                               initialfile="compressed.mp4")
    if not output_path:
        return

    try:
        # Compress video using FFmpeg
        (
            ffmpeg
            .input(file_path)
            .output(output_path, vcodec='libx264', crf=28)  # CRF 28 for reasonable compression
            .run()
        )
        messagebox.showinfo("Success", f"File compressed successfully!\nSaved as: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def handle_audio_conversion(file_path, bitrate, channels, sample_rate):
    if not file_path:
        messagebox.showerror("Error", "No file selected!")
        return

    # Choose output file path
    output_path = filedialog.asksaveasfilename(defaultextension=".mp3",
                                               filetypes=[("MP3 files", "*.mp3")],
                                               initialfile="audio.mp3")
    if not output_path:
        return

    try:
        # Map bitrate, channels, and sample rate from dropdown values
        bitrate_map = {
            "Best (320 kbps)": "320k",
            "Normal (128 kbps)": "128k",
            "Lowest (64 kbps)": "64k"
        }
        channels_map = {
            "Stereo (2 channels)": 2,
            "Mono (1 channel)": 1
        }
        sample_rate_map = {
            "Best (44100 Hz)": 44100,
            "Normal (22050 Hz)": 22050,
            "Lowest (11025 Hz)": 11025
        }

        bitrate_str = bitrate_map[bitrate]
        channels_int = channels_map[channels]
        sample_rate_int = sample_rate_map[sample_rate]

        # Extract and compress audio using FFmpeg
        (
            ffmpeg
            .input(file_path)
            .output(output_path, format='mp3', acodec='libmp3lame', audio_bitrate=bitrate_str, ac=channels_int, ar=sample_rate_int)
            .run()
        )
        messagebox.showinfo("Success", f"Audio extracted and compressed successfully!\nSaved as: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoCompressorGUI(root, handle_compression, handle_audio_conversion)
    root.mainloop()

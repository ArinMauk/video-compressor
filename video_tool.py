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
        # Convert input values to appropriate types
        bitrate_str = f"{bitrate}k"  # Bitrate in kbps
        channels_int = int(channels)
        sample_rate_int = int(sample_rate)

        # Extract and compress audio using FFmpeg
        (
            ffmpeg
            .input(file_path)
            .output(output_path, format='mp3', acodec='libmp3lame', audio_bitrate=bitrate_str, ac=channels_int, ar=sample_rate_int)
            .run()
        )
        messagebox.showinfo("Success", f"Audio extracted and compressed successfully!\nSaved as: {output_path}")
    except ValueError as ve:
        messagebox.showerror("Input Error", f"Please provide valid numeric values for bitrate, channels, and sample rate. Error: {str(ve)}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoCompressorGUI(root, handle_compression, handle_audio_conversion)
    root.mainloop()

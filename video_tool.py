import os
import ffmpeg
from tkinter import messagebox, filedialog
import tkinter as tk
from video_gui import VideoUtilityApp
import speech_recognition as sr
import tempfile


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


def handle_audio_to_text(file_path):
    if not file_path:
        messagebox.showerror("Error", "No file selected!")
        return

    try:
        recognizer = sr.Recognizer()
        temp_dir = tempfile.mkdtemp()  # Create a temporary directory to store audio chunks
        base_filename = os.path.splitext(os.path.basename(file_path))[0]
        
        # Split audio into 1-minute segments using FFmpeg
        chunk_output_pattern = os.path.join(temp_dir, f"{base_filename}_%03d.wav")
        (
            ffmpeg
            .input(file_path)
            .output(chunk_output_pattern, f='segment', segment_time='60', c='pcm_s16le')
            .run()
        )

        # List all audio chunks generated
        audio_chunks = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.endswith('.wav')]
        audio_chunks.sort()  # Sort to ensure sequential processing

        # Transcribe each chunk
        full_transcription = ""
        for chunk_file in audio_chunks:
            with sr.AudioFile(chunk_file) as source:
                audio_data = recognizer.record(source)
                try:
                    transcription = recognizer.recognize_google(audio_data)
                    full_transcription += transcription + "\n"
                except sr.UnknownValueError:
                    full_transcription += "[Unintelligible Audio]\n"
                except sr.RequestError:
                    messagebox.showerror("Error", "Could not request results from the speech recognition service.")
                    return

        # Save full transcription to file
        output_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                   filetypes=[("Text files", "*.txt")],
                                                   initialfile="transcription.txt")
        if not output_path:
            return

        with open(output_path, "w") as file:
            file.write(full_transcription)

        messagebox.showinfo("Success", f"Transcription saved successfully!\nSaved as: {output_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

    finally:
        # Clean up temporary files
        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))
        os.rmdir(temp_dir)

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoUtilityApp(root)

    # Attach the functions to the corresponding methods in VideoUtilityApp
    app.handle_compression = handle_compression
    app.handle_audio_conversion = handle_audio_conversion
    app.handle_audio_to_text = handle_audio_to_text

    root.mainloop()

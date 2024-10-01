import os
import wave
import vosk
import ffmpeg
import json
from tkinter import messagebox, filedialog
import tkinter as tk
from video_gui import VideoUtilityApp

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

    # Convert audio to WAV if needed
    wav_output_path = file_path.rsplit(".", 1)[0] + ".wav"
    try:
        # Convert MP3 to WAV using FFmpeg
        (
            ffmpeg
            .input(file_path)
            .output(wav_output_path, format='wav')
            .run()
        )
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during file conversion: {str(e)}")
        return

    try:
        # Load Vosk model (change the path to where you unzipped your Vosk model)
        model_path = r"C:\Users\arinm\OneDrive\Desktop\Software Development\Models\vosk-model-en-us-0.22\vosk-model-en-us-0.22"
        if not os.path.exists(model_path):
            messagebox.showerror("Error", "Vosk model not found. Please provide the correct model path.")
            return

        model = vosk.Model(model_path)

        # Open the WAV file
        with wave.open(wav_output_path, "rb") as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000, 22050, 44100]:
                messagebox.showerror("Error", "Audio file must be WAV format with a supported sample rate (8k, 16k, 22.05k, 44.1k Hz) and 16-bit.")
                return

            # Create a Vosk recognizer
            recognizer = vosk.KaldiRecognizer(model, wf.getframerate())

            # Transcribe the audio file
            full_transcription = ""
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    full_transcription += result.get("text", "") + "\n"
            # Process any remaining partial results
            result = json.loads(recognizer.FinalResult())
            full_transcription += result.get("text", "") + "\n"

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
        # Clean up WAV file after use if it was successfully created
        if os.path.exists(wav_output_path):
            os.remove(wav_output_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoUtilityApp(root)

    # Attach the functions to the corresponding methods in VideoUtilityApp
    app.handle_compression = handle_compression
    app.handle_audio_conversion = handle_audio_conversion
    app.handle_audio_to_text = handle_audio_to_text

    root.mainloop()

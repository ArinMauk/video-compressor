# Video Utility Tool

This is a simple Python application with a graphical user interface (GUI) that allows you to:
1. Compress video files.
2. Extract and compress audio from video files with customizable audio settings.

## Features
- Compress video files using FFmpeg.
- Convert video files into MP3 audio with customizable bitrate, channels, and sample rate.

## Prerequisites
- Python 3.12 or higher.
- FFmpeg installed on your system.
- The following Python packages:
  - `tkinter` (comes pre-installed with Python)
  - `ffmpeg-python`

### Installing FFmpeg Using Chocolatey
If you're on Windows, the easiest way to install FFmpeg is by using [Chocolatey](https://chocolatey.org/), a package manager for Windows.

1. **Install Chocolatey** (if not already installed):
   - Open PowerShell as an administrator and run the following command:
     ```powershell
     Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.WebClient]::new().DownloadString('https://community.chocolatey.org/install.ps1') | Invoke-Expression
     ```

2. **Install FFmpeg** using Chocolatey:
   - Open PowerShell as an administrator and run:
     ```powershell
     choco install ffmpeg
     ```
   - This will install FFmpeg and add it to your system's PATH, making it accessible from anywhere.

### Installing Python Dependencies
To install the required Python packages, run:

```
pip install ffmpeg-python
```

## Running the Application

### Clone the Repository:

```
git clone https://github.com/ArinMauk/video-compressor.git
```
### Run the Application:

```
python video_tool.py
```
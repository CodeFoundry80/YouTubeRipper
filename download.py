import os
import sys
import subprocess

if len(sys.argv) < 2:
    print("Usage: python download_lcd.py <YouTube_URL>")
    sys.exit(1)

url = sys.argv[1]

# Step 1: Download ONLY the single video into a temp file
print("⏳ Downloading from YouTube...")
subprocess.run([
    "yt-dlp",
    "--no-playlist",
    "-f", "bestvideo[height<=1080][vcodec^=avc1]+bestaudio[ext=m4a]/best[vcodec^=avc1]",
    "-o", "temp_input.%(ext)s",
    url
], check=True)

# Step 2: Get video title (yt-dlp can fetch it)
title = subprocess.check_output([
    "yt-dlp", "--get-title", "--no-playlist", url
], text=True).strip()

output_file = f"{title}.mp4"

print(f"🎞️ Converting for Corsair LCD... -> {output_file}")
subprocess.run([
    "ffmpeg", "-i", "temp_input.mp4",
    "-vf", "scale=480:480:force_original_aspect_ratio=decrease,fps=30",
    "-c:v", "libx264", "-pix_fmt", "yuv420p",
    "-preset", "fast", "-crf", "23",
    "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2",
    output_file, "-y"
], check=True)

# Step 3: Cleanup temp file
if os.path.exists("temp_input.mp4"):
    os.remove("temp_input.mp4")

print(f"✅ Done! File is ready: {output_file}")

import sys
import os
import subprocess
import re
import glob

def get_transcript(video_url_or_id):
    if not video_url_or_id.startswith("http"):
        url = f"https://www.youtube.com/watch?v={video_url_or_id}"
    else:
        url = video_url_or_id

    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        out_pattern = os.path.join(temp_dir, "%(id)s.%(ext)s")

        cmd = [
            "yt-dlp",
            "--skip-download",
            "--write-auto-sub",
            "--sub-lang", "en-orig,en-US-orig,en",
            "--output", out_pattern,
            url
        ]

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Find the downloaded vtt file
        vtt_files = glob.glob(os.path.join(temp_dir, "*.vtt"))
        if not vtt_files:
            return "No English transcript found."

        latest_file = max(vtt_files, key=os.path.getmtime)
        with open(latest_file, "r", encoding="utf-8") as f:
            content = f.read()

    # Clean up vtt
    lines = content.splitlines()
    cleaned = []
    seen = set()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:") or "-->" in line:
            continue
        # Remove tags like <00:00:00.335><c> etc.
        clean_line = re.sub(r"<[^>]+>", "", line).strip()
        if clean_line and clean_line not in seen:
            seen.add(clean_line)
            cleaned.append(clean_line)

    return " ".join(cleaned)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = get_transcript(sys.argv[1])
        print(text)

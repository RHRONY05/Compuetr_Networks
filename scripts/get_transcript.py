"""
Fetch a YouTube video's English captions and save them as a transcript file,
split into time-based parts so an agent can read long videos piece by piece.

The captions for the whole video are downloaded in one go (they already exist
on YouTube; nothing is transcribed from audio). The split is only for reading.

Usage:
    python scripts/get_transcript.py <URL or video id> [--part-minutes 30] [--print]

Output:
    .agents/transcripts/<video id>.md, with one "## Part N (start-end)" section
    per --part-minutes window (default 30). A short summary (title, length,
    file path, size of each part) is printed. --print also prints the full text.
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys
import tempfile

TRANSCRIPT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".agents", "transcripts")
TIME_RE = re.compile(r"(\d+):(\d{2}):(\d{2})\.(\d{3})\s+-->")


def to_url(video):
    return video if video.startswith("http") else f"https://www.youtube.com/watch?v={video}"


def fmt(seconds):
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def download(url, temp_dir):
    """Download captions + video info. Returns (vtt_path or None, info dict).

    Tries one caption track at a time (original English first). Asking for several
    at once makes YouTube rate-limit the extra ones, and yt-dlp then waits silently.
    """
    info = {}
    for lang in ("en-orig", "en-US-orig", "en"):
        cmd = [
            "yt-dlp", "--skip-download", "--write-auto-sub", "--write-info-json",
            "--sub-lang", lang, "--retries", "2", "--extractor-retries", "2",
            "--output", os.path.join(temp_dir, "%(id)s.%(ext)s"),
            url,
        ]
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
        except subprocess.TimeoutExpired:
            continue
        for path in glob.glob(os.path.join(temp_dir, "*.info.json")):
            with open(path, encoding="utf-8") as f:
                info = json.load(f)
        vtts = glob.glob(os.path.join(temp_dir, "*.vtt"))
        if vtts:
            return vtts[0], info
    return None, info


def parse_vtt(path):
    """Return [(start_seconds, text_line)] with timing tags and rolling repeats removed."""
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    out, recent, current = [], [], 0.0
    for raw in lines:
        line = raw.strip()
        m = TIME_RE.match(line)
        if m:
            h, mi, s, ms = map(int, m.groups())
            current = h * 3600 + mi * 60 + s + ms / 1000
            continue
        if not line or line.startswith(("WEBVTT", "Kind:", "Language:")):
            continue
        text = re.sub(r"<[^>]+>", "", line).strip()
        # Auto-captions repeat the previous line in the next cue; skip near repeats only,
        # so genuinely repeated phrases later in the video are kept.
        if not text or text in recent:
            continue
        out.append((current, text))
        recent = (recent + [text])[-5:]
    return out


def split_parts(entries, part_seconds):
    parts = {}
    for start, text in entries:
        parts.setdefault(int(start // part_seconds), []).append(text)
    return [(i, " ".join(parts[i])) for i in sorted(parts)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", help="YouTube URL or video id")
    ap.add_argument("--part-minutes", type=int, default=30, help="minutes per part (default 30)")
    ap.add_argument("--print", action="store_true", help="also print the full transcript")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    with tempfile.TemporaryDirectory() as temp_dir:
        vtt, info = download(to_url(args.video), temp_dir)
        if not vtt:
            print("No English transcript found (no captions, or YouTube rate-limited the request: wait a few minutes and retry).")
            sys.exit(1)
        entries = parse_vtt(vtt)

    video_id = info.get("id") or re.sub(r"\W", "_", args.video)[-20:]
    title = info.get("title", "(unknown title)")
    duration = info.get("duration") or (entries[-1][0] if entries else 0)
    part_seconds = args.part_minutes * 60
    parts = split_parts(entries, part_seconds)

    os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
    out_path = os.path.join(TRANSCRIPT_DIR, f"{video_id}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"- URL: {to_url(video_id)}\n- Length: {fmt(duration)}\n- Parts: {len(parts)} x {args.part_minutes} min\n\n")
        for n, (i, text) in enumerate(parts):
            end = duration if n == len(parts) - 1 else (i + 1) * part_seconds
            f.write(f"## Part {i + 1} ({fmt(i * part_seconds)}-{fmt(end)})\n\n{text}\n\n")

    print(f"Title:  {title}")
    print(f"Length: {fmt(duration)}")
    print(f"Saved:  {os.path.relpath(out_path)}")
    for n, (i, text) in enumerate(parts):
        end = duration if n == len(parts) - 1 else (i + 1) * part_seconds
        print(f"  Part {i + 1} ({fmt(i * part_seconds)}-{fmt(end)}): {len(text):,} characters")
    print("Read the file part by part (each '## Part' heading starts a new section).")

    if args.print:
        print()
        print("\n\n".join(text for _, text in parts))


if __name__ == "__main__":
    main()

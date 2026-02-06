# ================================================================
# 0. Section: IMPORTS
# ================================================================
import subprocess
import json

from pathlib import Path



# ================================================================
# 1. Section: Find errors
# ================================================================
def ffmpeg_needs_fix(video_path: Path) -> bool:
    # 1) sequential decode errors
    cmd = ["ffmpeg", "-hide_banner",
        "-v", "error",
        "-i", str(video_path),
        "-map", "0:v:0",
        "-f", "null", "-"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.stderr.strip():
        return True

    # 2) frame count mismatch => random access likely broken
    nb_frames, nb_read_frames = ffprobe_frame_counts(video_path)
    if nb_frames is not None and nb_read_frames is not None and nb_read_frames < nb_frames:
        return True

    return False



# ================================================================
# 2. Section: Fix Cropping and Stiching
# ================================================================
def ffmpeg_fix_stich_crop_mp4(input_path: Path, output_folder: Path) -> Path:
    output_folder.mkdir(parents=True, exist_ok=True)
    output_path = output_folder / f"{input_path.stem}.mp4"

    cmd = ["ffmpeg", "-hide_banner",
        "-y" if False else "-n",
        "-i", str(input_path),
        "-map", "0"]

    fps = get_video_fps_ffprobe(input_path)
    if fps is not None:
        cmd += ["-vf", f"fps={fps}"]  # CFR makes frame indexing stable

    cmd += [
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-movflags", "+faststart",
        str(output_path),
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True)

    if proc.returncode != 0:
        raise RuntimeError(
            "ffmpeg failed\n"
            f"command: {' '.join(cmd)}\n"
            f"stderr:\n{proc.stderr.strip()}"
        )

    if not output_path.exists() or output_path.stat().st_size == 0:
        raise RuntimeError(f"ffmpeg reported success but output is missing/empty: {output_path}")

    #print(f"Success fixing: {output_path}")
    return output_path



# ──────────────────────────────────────────────────────
# 1.1 Subsection: Helper Functions
# ──────────────────────────────────────────────────────
def ffprobe_frame_counts(video_path: Path) -> tuple[int | None, int | None]:
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-count_frames",
        "-show_entries", "stream=nb_frames,nb_read_frames",
        "-of", "json",
        str(video_path),
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        return None, None

    data = json.loads(p.stdout)
    streams = data.get("streams", [])
    if not streams:
        return None, None

    s = streams[0]
    def to_int(x):
        try:
            return int(x)
        except (TypeError, ValueError):
            return None

    return to_int(s.get("nb_frames")), to_int(s.get("nb_read_frames"))


def get_video_fps_ffprobe(video_path: Path) -> float:
    p = Path(video_path).expanduser()

    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=avg_frame_rate,r_frame_rate",
        "-of", "json",
        str(p),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffprobe failed:\n{proc.stderr.strip()}")

    data = json.loads(proc.stdout)
    streams = data.get("streams", [])
    if not streams:
        raise ValueError(f"No video stream found in {p}")

    s = streams[0]
    rate = s.get("avg_frame_rate") or s.get("r_frame_rate")
    if not rate or rate == "0/0":
        raise ValueError(f"Could not determine fps for {p} (rate={rate!r})")

    num_str, den_str = rate.split("/")
    num = float(num_str)
    den = float(den_str)
    if den == 0:
        raise ValueError(f"Invalid fps fraction {rate!r} for {p}")

    return num / den

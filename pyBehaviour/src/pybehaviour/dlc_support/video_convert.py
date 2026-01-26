# ================================================================
# 0. Section: IMPORTS
# ================================================================
import subprocess
import os

from pathlib import Path

MP4_VIDEO_CODEC = "libx265"
MP4_AUDIO_CODEC = "aac"
MP4_AB = "192k"
X265_CRF = "24"
X265_PRESET = "medium"

# AVI settings (optional)
AVI_VIDEO_CODEC = "mpeg4"          # could also be "libxvid"
AVI_AUDIO_CODEC = "libmp3lame"



# ================================================================
# 1. Section: Convertion Functions
# ================================================================
def convert_mov(mov_path: Path, out_folder: Path, out_ext: str) -> None:
    # 1. Builds the paths
    os.makedirs(out_folder, exist_ok=True)
    file_name = mov_path.stem
    out_path = out_folder / file_name
    out_path = out_path.with_suffix(f".{out_ext}")

    # 2. Applies the correct convertion
    if out_ext.lower() == "mp4":
        rc, out = mov2mp4(mov_path, out_path)
    elif out_ext.lower() == "avi":
        rc, out = mov2avi(mov_path, out_path)
    else:
        raise ValueError("OUTPUT_FORMAT must be 'mp4' or 'avi'")

    # 3. Asserts it worked
    if rc != 0:
        print("\nConversion FAILED:")
        print(out.strip())
        return


# ──────────────────────────────────────────────────────
# 1.1 Subsection: Helpers for Convertion
# ──────────────────────────────────────────────────────
def run_capture(cmd: list[str]) -> tuple[int, str]:
    """Run command, return (returncode, combined stdout+stderr)."""
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return p.returncode, p.stdout

def mov2mp4(mov_path: Path, out_path: Path) -> tuple:
    cmd_enc = [
        "ffmpeg", "-y", "-i", str(mov_path),
        "-c", "copy",
        "-movflags", "+faststart",
        str(out_path),
    ]
    """
    # Full recompile (maybe not needed)
    cmd_enc = [
        "ffmpeg", "-y", "-i", str(mov_path),
        "-c:v", MP4_VIDEO_CODEC, "-crf", X265_CRF, "-preset", X265_PRESET,
        "-c:a", MP4_AUDIO_CODEC, "-b:a", MP4_AB,
        "-movflags", "+faststart",
        str(out_path),
    ]
    """
    rc, out = run_capture(cmd_enc)

    return rc, out

def mov2avi(mov_path: Path, out_path: Path) -> tuple:
    # AVI variant (mpeg4 + mp3 by default here)
    cmd_avi = [
        "ffmpeg", "-y", "-i", str(mov_path),
        "-c:v", AVI_VIDEO_CODEC, "-q:v", "5",
        "-c:a", AVI_AUDIO_CODEC, "-q:a", "4",
        str(out_path),
    ]
    rc, out = run_capture(cmd_avi)

    return rc, out



# ================================================================
# 2. Section: CODEC Functions
# ================================================================
def ffprobe_codecs(path: Path, video_only: bool = False) -> str:
    """Return a readable summary of codecs inside a media file."""
    cmd = ["ffprobe", "-v", "error"]
    if video_only:
        cmd += ["-select_streams", "v:0"]
    cmd += [
        "-show_entries", "stream=codec_type,codec_name",
        "-of", "default=nw=1",
        str(path),
    ]
    rc, out = run_capture(cmd)
    if rc != 0:
        return f"(ffprobe failed)\n{out.strip()}"
    return out.strip()

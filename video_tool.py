import os
import subprocess
from pathlib import Path


class UnsupportedVideoFormatError(Exception):
    def __init__(self, format_name: str):
        super().__init__(f"Unsupported Video format: {format_name}")


def path_exists(path: str) -> bool:
    return os.path.exists(path)


def is_file(path: str) -> bool:
    return os.path.isfile(path)


def extract_options(options: dict) -> dict:
    """
        Extracts valid video and audio conversion options from the given dictionary.

        Args:
            options (dict): A dictionary containing various conversion options.

        Returns:
            dict: A filtered dictionary containing valid options for video and audio conversion.

        Example:
            options = {
                "resolution": "1280:720",
                "video_codec": "libx264",
                "audio_codec": "aac",
                "bitrate": 192,
                "fps": 30,
            }
            valid_options = extract_options(options)
            # valid_options will contain only the valid options based on predefined lists.
        """
    valid_options = {}

    resolutions_list = ["320:240", "640:480", "1280:720", "1920:1080", "2560:1440", "3840:2160"]
    codec_list = ["copy", "libx264", "libx265", "av1"]
    preset_list = ["veryslow", "slower", "slow", "medium", "fast", "veryfast", "superfast", "ultrafast"]
    tune_list = ["film", "animation", "grain", "stillimage", "psnr", "ssim", "fastdecode", "zerolatency"]
    crf = range(0, 51)
    fps = range(15, 120)

    audio_codec_list = ["copy", "aac", "ac3", "flac", "libmp3lame"]
    bitrate = range(128, 320)
    channel = {"stereo": 2, "mono": 1}
    sample_rates = ["8000", "11025", "16000", "22050", "32000", "44100", "48000", "88200", "96000"]
    volume = range(-50, 100)

    for key, value in options.items():
        # Video options
        if key == "resolution" and value in resolutions_list:
            valid_options[key] = value
        elif key == "codec" and value in codec_list:
            valid_options[key] = value
        elif key == "preset" and value in preset_list:
            valid_options[key] = value
        elif key == "tune" and value in tune_list:
            valid_options[key] = value
        elif key == "crf" and value in crf:
            valid_options[key] = str(value)
        elif key == "fps" and value in fps:
            valid_options[key] = str(value)
        # Audio options
        elif key == "audio_codec" and value in audio_codec_list:
            valid_options[key] = value
        elif key == "bitrate" and value in bitrate:
            valid_options[key] = f"{value}k"
        elif key == "channel" and value in channel:
            valid_options[key] = str(channel[value])
        elif key == "sample_rates" and value in sample_rates:
            valid_options[key] = value
        elif key == "volume" and value in volume:
            valid_options[key] = str(value)

    return valid_options


def video_converter(input_path: str, output_path: str, target_format: str, options: dict) -> bool:
    """
        Converts a video file from one format to another using FFmpeg.

        Args:
            input_path (str): Path to the input video file.
            output_path (str): Path to the output folder where the converted video will be saved.
            target_format (str): Target video format (e.g., "mp4", "mkv").
            options (dict): Dictionary containing video and audio conversion options.

        Raises:
            FileExistsError: If the input file does not exist.
            NotADirectoryError: If the output folder does not exist.
            UnsupportedVideoFormatError: If the target format is not supported.

        Returns:
            bool: True if conversion successful otherwise False.

        Example:
            options = {
                "resolution": "1280:720",
                "video_codec": "libx264",
                "audio_codec": "aac",
                "bitrate": "192",
                "fps": "30",
            }
            video_converter("input.mp4", "output_folder", "mp4", options)
        """
    if not is_file(input_path):
        raise FileExistsError(f"File {input_path} does not exists.")

    if not path_exists(output_path):
        raise NotADirectoryError(f"Output folder {output_path} does not exists.")

    target_format = target_format.lower().strip()

    video_formats = [
        "avi",
        "flv",
        "mkv",
        "mov",
        "mp4",
        "webm",
        "wmv"
    ]

    if target_format.lower() not in video_formats:
        raise UnsupportedVideoFormatError(target_format)

    filename, extension = os.path.splitext(os.path.basename(input_path))
    output_name = str(Path(output_path) / f"{filename}_converted.{target_format}")

    get_options = extract_options(options)

    ffmpeg_command = ["ffmpeg", "-i", input_path]

    for key, value in get_options.items():
        if key == "resolution":
            ffmpeg_command.extend(["-vf", f"scale={value}"])
        elif key == "video_codec":
            ffmpeg_command.extend(["-c:v", value])
        elif key == "preset":
            ffmpeg_command.extend(["-preset", value])
        elif key == "tune":
            ffmpeg_command.extend(["-tune", value])
        elif key == "crf":
            ffmpeg_command.extend(["-crf", value])
        elif key == "fps":
            ffmpeg_command.extend(["-r", value])

        elif key == "audio_codec":
            ffmpeg_command.extend(["-c:a", value])
        elif key == "bitrate":
            ffmpeg_command.extend(["-b:a", value])
        elif key == "channel":
            ffmpeg_command.extend(["-ac", value])
        elif key == "sample_rates":
            ffmpeg_command.extend(["-ar", value])
        elif key == "volume":
            ffmpeg_command.extend(["-af", f"volume={value}dB"])

    ffmpeg_command.append(output_name)

    try:
        subprocess.run(ffmpeg_command)
        return True
    except Exception as e:
        print(f"Error converting {input_path}: {e}")
        return False

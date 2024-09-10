# VideoConverter
Convert video files to other video formats with custom options using ffmpeg.

## Example

```python
from video_converter import convert_video

def success_callback(msg: str) -> None:
    print(msg)


def failure_callback(msg: str) -> None:
    print(msg)


input_video = "path\\to\\input.mp4"
output_video = "path\\to\\output"
output_format = "mp4"
video_options = {"resolution": "1920:1080", "codec": "libx264", "preset": "medium", "tune": "film", "crf": 23,
                 "fps": 60, "audio_codec": "aac", "bitrate": 192, "channel": "stereo", "sample_rate": "48000",
                 "volume": 0}

# Usage
convert_video(input_video, output_video, output_format, success_callback, failure_callback, **video_options)
```

## Options
- Supported formats: [avi, flv, mkv, mov, mp4, webm, wmv]
- Resolutions = [320:240, 640:480, 1280:720, 1920:1080, 2560:1440, 3840:2160]
- Codec = [copy, libx264, libx265, av1]
- Preset = [veryslow, slower, slow, medium, fast, veryfast, superfast, ultrafast]
- Tune = [film, animation, grain, stillimage, psnr, ssim, fastdecode, zerolatency]
- Crf = 0 - 51
- Fps = 15 - 120

- Audio codec = [copy, aac, ac3, flac, libmp3lame]
- Bitrate = 128 - 320
- Channel = [stereo, mono]
- Sample rates = [8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000]
- Volume = 0 - 100

Make sure you have installed ffmpeg on your system! 
https://www.ffmpeg.org/download.html


###

<h2 align="left">Support</h2>

###

<p align="left">If you'd like to support my ongoing efforts in sharing fantastic open-source projects, you can contribute by making a donation via PayPal.</p>

###

<div align="center">
  <a href="https://www.paypal.com/paypalme/iamironman0" target="_blank">
    <img src="https://img.shields.io/static/v1?message=PayPal&logo=paypal&label=&color=00457C&logoColor=white&labelColor=&style=flat" height="40" alt="paypal logo"  />
  </a>
</div>

###

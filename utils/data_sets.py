VIDE_EXTENSIONS = [
    'webm', 'mkv', 'flv', 'vob', 'ogv', 'ogg', 'rrc', 'gifv', 'mng',
    'mov', 'avi', 'qt', 'wmv', 'yuv', 'rm', 'asf', 'amv', 'mp4', 'm4p',
    'm4v', 'mpg', 'mp2', 'mpeg', 'mpe', 'mpv', 'm4v', 'svi', '3gp',
    '3g2', 'mxf', 'roq', 'nsv', 'flv', 'f4v', 'f4p', 'f4a', 'f4b', 'mod',
]

SUBTITLE_EXTENSIONS = ['srt']

IMAGE_EXTENSIONS = [
    "jpg", "jpeg", "png", "gif", "bmp", "tiff", "tif", "webp",
    "svg", "ico", "heic", "heif", "raw", "cr2", "nef", "arw",
    "psd", "ai", "eps"
]

TEXT_EXTENSIONS = ['txt', 'text', 'md', 'nfo']


def file_extensions() -> list:
    """Return a list of file extensions known to be encountered."""
    # Return a list of common video extensions.
    return VIDE_EXTENSIONS + SUBTITLE_EXTENSIONS + IMAGE_EXTENSIONS + TEXT_EXTENSIONS


def video_qualities() -> list:
    # Return a list of video qualities.
    return [
        '240p', '360p', '480p', '720p', '1080p', '1440p', '2160p', '4320p'
    ]


def exit_list() -> list:
    return ['exit', 'quit']
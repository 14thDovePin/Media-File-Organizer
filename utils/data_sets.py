def file_extensions() -> list:
    """Return a list of file extensions known to be encountered."""
    # Return a list of common video extensions.
    return [
        # Video extensions
        'webm', 'mkv', 'flv', 'vob', 'ogv', 'ogg', 'rrc', 'gifv', 'mng',
        'mov', 'avi', 'qt', 'wmv', 'yuv', 'rm', 'asf', 'amv', 'mp4', 'm4p',
        'm4v', 'mpg', 'mp2', 'mpeg', 'mpe', 'mpv', 'm4v', 'svi', '3gp',
        '3g2', 'mxf', 'roq', 'nsv', 'flv', 'f4v', 'f4p', 'f4a', 'f4b', 'mod',

        # Subtitiles
        'srt'
    ]


def video_qualities() -> list:
    # Return a list of video qualities.
    return [
        '240p', '360p', '480p', '720p', '1080p', '1440p', '2160p', '4320p'
    ]

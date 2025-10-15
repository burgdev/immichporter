from enum import Enum


class AudioCodec(str, Enum):
    AAC = "aac"
    LIBOPUS = "libopus"
    MP3 = "mp3"
    PCM_S16LE = "pcm_s16le"

    def __str__(self) -> str:
        return str(self.value)

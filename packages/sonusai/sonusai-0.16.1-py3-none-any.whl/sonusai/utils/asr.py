from dataclasses import dataclass
from typing import Any
from typing import Callable
from typing import Optional

from sonusai.mixture import AudioT


@dataclass(frozen=True)
class ASRData:
    audio: AudioT
    whisper_model: Optional[Any] = None
    whisper_model_name: Optional[str] = None
    device: Optional[str] = None
    cpu_threads: Optional[int] = None
    compute_type: Optional[str] = None
    beam_size: Optional[int] = None


@dataclass(frozen=True)
class ASRResult:
    text: str
    confidence: Optional[float] = None
    lang: Optional[str] = None
    lang_prob: Optional[float] = None
    duration: Optional[float] = None
    num_segments: Optional[int] = None
    asr_cpu_time: Optional[float] = None


def get_available_engines() -> dict[str, Callable[[ASRData], ASRResult]]:
    from importlib import import_module
    from pkgutil import iter_modules

    module = import_module('sonusai.utils.asr_functions')
    engines = {method: getattr(module, method) for method in dir(module) if not method.startswith('_')}
    for _, name, _ in iter_modules():
        if name.startswith('sonusai_asr_'):
            module = import_module(f'{name}.asr_functions')
            for method in dir(module):
                if not method.startswith('_'):
                    engines[method] = getattr(module, method)

    return engines


def calc_asr(audio: AudioT | str,
             engine: Optional[str] = 'aaware_whisper',
             whisper_model: Optional[Any] = None,
             whisper_model_name: Optional[str] = 'tiny',
             device: Optional[str] = 'cpu',
             cpu_threads: Optional[int] = 1,
             compute_type: Optional[str] = 'int8',
             beam_size: Optional[int] = 5) -> ASRResult:
    """Run ASR on audio

    :param audio: Numpy array of audio samples or location of an audio file
    :param engine: Type of ASR engine to use
    :param whisper_model: A preloaded Whisper ASR model
    :param whisper_model_name: Name of Whisper ASR model to use if none was provided
    :param device: the device to put the ASR model into
    :param cpu_threads: int specifying threads to use when device is cpu
           note: must be 1 if this func is run in parallel
    :param compute_type: the precision of ASR model to use
    :param beam_size: int specifying beam_size to use
    :return: ASRResult object containing text and confidence
    """
    from copy import copy

    import numpy as np

    from sonusai import SonusAIError
    from sonusai.mixture import read_audio

    available_engines = get_available_engines()
    if engine not in available_engines:
        raise SonusAIError(f'Unsupported ASR function: {engine}')

    if not isinstance(audio, np.ndarray):
        audio = copy(read_audio(audio))

    data = ASRData(audio, whisper_model, whisper_model_name, device, cpu_threads, compute_type, beam_size)

    return available_engines[engine](data)

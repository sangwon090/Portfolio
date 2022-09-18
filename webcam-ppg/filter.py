import numpy as np
import scipy.signal as signal
import scipy.fftpack as fftpack

from enum import Enum

class Filter(Enum):
    IDEAL = 0,
    BUTTERWORTH = 1,
    IIR = 2,

def ideal_filter(video: np.ndarray, fps: int, low: float, high: float, axis: int = 0):
    fft = np.fft.fft(video, axis=axis)
    freq = np.fft.fftfreq(video.shape[0], d=1.0/fps)
    bound_low = (np.abs(freq - low)).argmin()
    bound_high = (np.abs(freq - high)).argmin()
    fft[:bound_low] = 0
    fft[bound_high:-bound_high] = 0
    fft[-bound_low:] = 0
    ifft = np.fft.ifft(fft, axis=axis)
    result = np.abs(ifft)

    return result

def butterworth_filter(video: np.ndarray, fps: int, low: float, high: float, axis: int = 0, order: int = 5):
    omega = fps / 2.0
    low /= omega
    high /= omega
    b, a = signal.butter(order, [low, high], btype='band')
    y = signal.lfilter(b, a, video, axis)

    return y

def iir_filter(video: np.ndarray):

    return video

def filter(video: np.ndarray, filter: Filter, fps: int, low: float, high: float):
    match filter:
        case Filter.IDEAL:
            return ideal_filter(video, fps, low, high)
        case Filter.BUTTERWORTH:
            return butterworth_filter(video, fps, low, high)
        case Filter.IIR:
            return iir_filter(video, fps, low, high)
        case _:
            return video
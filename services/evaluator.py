from models.declarative_models import MotorEvaluateStandard
from numpy import ndarray
import numpy as np
from scipy import signal

class ElectricSignal:
    def __init__(self, signal:bytes):
        self.data = signal
        self.dedata = None
        self.dtype = np.float32
        self.rate = 20480
        self.time_axis = None
        self.spec = None
        self.freq_axis = None
        self.preprocess()


    def __len__(self):
        return self.dedata.shape[0]

    def preprocess(self):
        self._deserialize()
        self._detrend()

    def _deserialize(self):
        self.dedata = np.fromstring(self.data, dtype=self.dtype)

    def _detrend(self):
        self.dedata = signal.detrend(self.dedata)

    def compute_timeaxis(self):
        self.time_axis = np.linspace(0, len(self)/self.rate, len(self))

    def compute_fft(self):
        spec = np.fft.fft(self.dedata)[0:int(len(self) / 2)] / len(self)  # FFT function from numpy
        spec[1:] = 2 * spec[1:]  # need to take the single-sided spectrum only
        self.spec =  np.abs(spec)

class MotorDiagnosis:

    def __init__(self, u: ndarray, v: ndarray, w: ndarray):
        self.signal = [u,v,w]
        self.fft = []
        self.rate = 20480
        self.lenth = u.shape[0]
        self.freq_interval = self.rate / 2 / (self.lenth / 2)

        self._init_fft()

    def _init_fft(self):
        for item in self.signal:
            self.fft.append(self.compute_fft(item))

    def compute_fft(self, signal: ndarray):
        spec = np.fft.fft(signal)[0:int(self.lenth / 2)] / self.lenth  # FFT function from numpy
        spec[1:] = 2 * spec[1:]  # need to take the single-sided spectrum only
        return np.abs(spec)
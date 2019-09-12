import numpy as np
from numpy import ndarray


def threephase_deserialize(u, v, w):
    return np.fromstring(u, dtype=np.float32), np.fromstring(v, dtype=np.float32), np.fromstring(w, dtype=np.float32)


def dq0_transform(v_a, v_b, v_c):
    d = (np.sqrt(2 / 3) * v_a - (1 / (np.sqrt(6))) * v_b - (1 / (np.sqrt(6))) * v_c)
    q = ((1 / (np.sqrt(2))) * v_b - (1 / (np.sqrt(2))) * v_c)
    return d, q


def cal_samples(phaseAOmega, phaseBOmega, phaseCOmega, end_time):
    '''
    Calculate the number of samples needed.
    '''
    max_omega = max(abs(phaseAOmega),
                    abs(phaseBOmega),
                    abs(phaseCOmega))
    max_freq = max_omega / (2 * np.pi)
    samples = (max_freq ** 2) * 6 * end_time
    return samples


def make_phase(mag, omega, phi, samples, end_time):
    '''
    Create the phase signal in complex form.
    '''

    array_time = np.linspace(0, end_time, samples)

    x = omega * array_time + phi

    return to_complex(mag, x), array_time


def cal_symm(a, b, c):
    # 120 degree rotator
    ALPHA = np.exp(1j * 2 / 3 * np.pi)

    # Positive sequence
    a_pos = 1 / 3 * (a + b * ALPHA + c * (ALPHA ** 2))

    b_pos = 1 / 3 * (a * (ALPHA ** 2) + b + c * ALPHA)

    c_pos = 1 / 3 * (a * ALPHA + b * (ALPHA ** 2) + c)

    # Negative sequence
    a_neg = 1 / 3 * (a + b * (ALPHA ** 2) + c * ALPHA)

    b_neg = 1 / 3 * (a * ALPHA + b + c * (ALPHA ** 2))

    c_neg = 1 / 3 * (a * (ALPHA ** 2) + b * ALPHA + c)

    # zero sequence
    zero = 1 / 3 * (a + b + c)

    return a_pos, b_pos, c_pos, a_neg, b_neg, c_neg, zero


def to_complex(r, x, real_offset=0, imag_offset=0):
    real = r * np.cos(x) + real_offset

    imag = r * np.sin(x) + imag_offset

    return (real + 1j * imag)


def fftransform(Signal: ndarray):
    # fft_size = int(Signal.shape[0])
    N = Signal.shape[0]
    spec = np.fft.fft(Signal)[0:int(N / 2)] / N  # FFT function from numpy
    spec[1:] = 2 * spec[1:]  # need to take the single-sided spectrum only
    spec = np.abs(spec)

    return spec


def db2percentage(db: float):
    return 100.0 / (10.0 ** (db / 20.0))

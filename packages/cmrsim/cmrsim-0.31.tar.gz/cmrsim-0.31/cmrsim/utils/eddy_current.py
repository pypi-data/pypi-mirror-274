""" Module containing utility to handle and incorporated Gradient Response Function (GIRF)
data and eddy current related computations
"""

import numpy as np

def apply_girf(gradient: np.ndarray, girf_terms: np.array , grad_padsize: int) -> np.ndarray:
    """Computes the gradient waveform terms for a given gradient and a gradient response 
    function (GIRF) of the gradient system. 

    Computation is performed by convolving the temporal representation of the MTF 
    with gradient waveform.
    
    :param gradient: Gradient waveform of shape (3, #timesteps) assumed to be 
                     specified on a regular time grid
    :param girf_terms: Modulation transfer function (MTF) of the gradient system
                       of shape (time, #terms, XYZ). Where the 1st axis (0-based)
                       contains the terms of spatial harmonics. Shapes correspondingly are
                       For 0th order -> (time, 1, 3)
                       For 1st order -> (time, 4, 3) 
                       For 2nd order -> (time, 9, 3)
                       For 3rd order -> (time, 16, 3)
    :param grad_padsize: Array padding before convolving the MTF with the gradient 
                         waveform
    :return: Eddy current affected gradient waveform defined as coefficients of the 
             spatial harmonics, of shape (#Time, #terms)
    """
    padded_gradient = [np.pad(g, (grad_padsize, grad_padsize)) for g in gradient]

    girf_terms_abs = np.abs(girf_terms).transpose(1, 0, 2)  # after: (terms, freq, XYZ)
    crop = int((girf_terms_abs.shape[0] - gradient.shape[1])/2)

    n_terms = girf_terms.shape[1]    
    result = np.zeros(gradient.shape[0], n_terms)
    for idx, girf_term in enumerate(girf_terms_abs):
        for i in range(3):
            result[idx] += scipy.signal.convolve(girf_term[:, i], padded_gradient[i], 
                                                 mode='same', method='direct')[crop:-crop]
    return result
            

def apply_girf_nonuniform(gradient: np.ndarray, t_grad: np.ndarray, girf_freq_def: np.ndarray,
    girf_terms: np.ndarray, grad_raster: float, grad_padsize: int):
    """Computes the gradient waveform terms for a given gradient and a gradient response 
    function (GIRF) of the gradient system. 

    Computation is performed by multiplying in frequency domain. 
    
    :param gradient: Gradient waveform of shape (#timesteps, 3)
    :param t_grad: Array containing the temporal definition of the gradient waveforms
    :param girf_freq_def: Frequency definition of the girf terms
    :param girf_terms: Modulation transfer function (MTF) of the gradient system
                       of shape (time, #terms, XYZ). Where the 1st axis (0-based)
                       contains the terms of spatial harmonics. Shapes correspondingly are
                       For 0th order -> (time, 1, 3)
                       For 1st order -> (time, 4, 3) 
                       For 2nd order -> (time, 9, 3)
                       For 3rd order -> (time, 16, 3)
    :param grad_raster: Raster time used to interpolate waveform onto for FFT in milliseconds
    :param grad_padsize: Array padding before convolving the MTF with the gradient 
                         waveform
    :return: Eddy current affected gradient waveform defined as coefficients of the 
             spatial harmonics, of shape (#Time, #terms)
    """
    # interpolate onto regular grid
    t_interp = np.arange(t_grad[0], t_grad[-1]+grad_raster, grad_raster)
    gradient_interp = [np.interp(t_interp, t_grad, g) for g in gradient.T]
    gradient_padded = [np.pad(g, (grad_padsize, grad_padsize)) for g in gradient_interp]
    gradient_spectrum = [np.fft.ifftshift(np.fft.fft(g)) for g in gradient_padded]
    frequency_interp = np.fft.ifftshift(np.fft.fftfreq(gradient_padded[0].shape[0], grad_raster))


    result = np.zeros((t_grad.shape[0], girf_terms.shape[1]))
    for idx, girf_term in enumerate(girf_terms.transpose(1, 2, 0)):
        girf_interp = [np.interp(frequency_interp, girf_freq_def, g) for g in girf_term]
        tmp = np.stack([grad_f * mtf for grad_f, mtf in zip(gradient_spectrum, girf_interp)])
        tmp = np.fft.ifft(np.fft.fftshift(np.sum(tmp, axis=0)))
        tmp = tmp[grad_padsize:-grad_padsize]
        result[:, idx] = np.real(np.interp(t_grad, t_interp, tmp))
    return result
    
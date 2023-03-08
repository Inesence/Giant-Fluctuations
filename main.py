import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.signal import find_peaks
from pathlib import Path
import xlsxwriter
import getpass
from openpyxl import Workbook

def read_image(file_path):
    """Reads an image file from the given path and returns it as a NumPy array."""
    img = mpimg.imread(file_path)
    return img

def crop_image(img, x1, x2, y1, y2):
    """Crops the given image array to the specified rectangle."""
    cropped_img = img[y1:y2, x1:x2]
    return cropped_img

def calculate_power_spectrum(img):
    """Calculates the power spectrum of the given image."""
    # Perform a Fourier transform:
    f = np.fft.fft2(img)
    
    # Shift Fourier transform to the center
    fshift = np.fft.fftshift(f)
    
    # Magnitude spectrum
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    
    # Absolute value of Fourier transform shift
    fshift_abs = np.abs(fshift)
    
    # Fourier transform squared (i.e., power spectrum)
    power_spectrum = fshift_abs ** 2
    
    return power_spectrum

def calculate_radial_profile(img):
    """Calculates the radial profile of the given image's power spectrum."""
    # Create array of radii
    x,y = np.meshgrid(np.arange(img.shape[1]), np.arange(img.shape[0]))
    R = np.sqrt((x - img.shape[1]//2)**2 + (y - img.shape[0]//2)**2)
    
    # Calculate the mean at each radius
    r = np.linspace(1, 200, num=200)
    k = lambda r_ : img[(R >= r_-0.5) & (R < r_+0.5)].mean()
    mean = np.vectorize(k)(r)
    
    return r, mean

def find_peak(r, mean, threshold):
    """Finds the first peak in the given radial profile above the given threshold."""
    peaks, _ = find_peaks(mean, height=threshold)
    if len(peaks) == 0:
        return None
    else:
        return r[peaks[0]], mean[peaks[0]]

def save_to_excel(data, sheet_name, file_path):
    """Saves the given data to an Excel file at the specified path and sheet name."""
    wb = Workbook()
    ws = wb.create_sheet(sheet_name)
    for row in data:
        ws.append(row)
    wb.save(file_path)

def process_directory(directory_path, x1, x2, y1, y2, threshold, output_file_path):
    """Processes all TIFF files in the specified directory and saves the results to an Excel file."""
    data = [('Radius', 'Mean')]
    for file_path in Path(directory_path).rglob('*.tif'):
        img = read_image(str(file_path))
        cropped_img = crop_image(img, x1, x2, y1, y2)
                power_spectrum = calculate_power_spectrum(cropped_img)
        r, mean = calculate_radial_profile(power_spectrum)
        peak = find_peak(r, mean, threshold)
        if peak:
            data.append(peak)
    save_to_excel(data, 'Sheet1', output_file_path)

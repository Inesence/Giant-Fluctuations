# Giant-Fluctuations: Image Analysis Code

This repository contains Python code for analyzing TIFF image files. The code includes various image processing techniques such as cropping, Fourier transform, power spectrum calculation, radial profile calculation, and peak detection.

## Requirements

To run this code, you will need the following Python packages:

* NumPy
* Matplotlib
* Scipy
* Pathlib
* Xlsxwriter
* Getpass
* Openpyxl

## Usage

To use the code, clone this repository and install the required packages. Then, run the `process_directory()` function with the following parameters:

* `directory_path`: The path to the directory containing the TIFF files to be analyzed.
* `x1`, `x2`, `y1`, `y2`: The rectangular area to be cropped from each image.
* `threshold`: The threshold value to use when finding the peak in the radial profile.
* `output_file_path`: The path where the Excel file containing the analysis results will be saved.

The output of the analysis is saved to an Excel file in the specified `output_file_path` location. The output file will have two columns: Radius and Mean. The `process_directory()` function processes all TIFF files in the specified directory and saves the results to the output Excel file.

## Contributing

If you would like to contribute to this code, feel free to submit a pull request with your changes. Please make sure to follow the existing coding style and include tests for any new functionality.

## License

Feel free to use it for your own research or projects.

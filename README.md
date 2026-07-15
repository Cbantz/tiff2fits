# About

tiff2fits is a Python/CLI utility to convert Tag Image File Format (.tif or .tiff) files to flexible image transport system (.FTS) files.

# Highlights

- Usable as a CLI or python package.
- Free and open source using the MIT License.

# Getting Started

tiff2fits can be installed from this repo using pip.

`pip install git+https://github.com/Cbantz/tiff2FITS.git`

After installation, you can use tiff2fits as a command line interface (CLI) or as a python package.

## Using CLI

Using the CLI takes a basic command structure:

`tiff2fits [input_path] [output_path] [args]`

- \[input_path\] is a path to either a .tiff file or a directory containing .tiff files that you wish to be converted.
- \[output_path\] is the location you wish the .FTS file to be saved. It can be either a directory (recommended) or a file path.
- \[args\]
    - \--overwrite will overwrite any existing files with the same name in an output path when saving your converted files.
    - \--verbose will print confirmations of each image as it is converted and saved.
    - \--compress is on by default but can be set to False if desired. It will save a lossless compression algorithm to save storage space, but has the effect saving in the 1st rather than in the 0th index of the HDU List.


**NOTES:**

- Currently, if given a directory as an \[input_path\], the CLI will convert all .tiff files in said directory.
- Cannot currently save both a compressed version and uncompressed in the same HDU List.
- If a directory is given for the \[output_path\], files will be saved as their original name but with .FTS instead of .tiff
    - e.g. input_path/image.tiff -> output_path/image.FTS
- You will get an error if you try to overwrite without using the overwrite flag.

## Using Python Package

tiff2fits can be imported into your project using

`from tiff2fits import tiff2fits`.

The only function you are likely to use is tiff2fits.convert().

This function, much like the CLI, takes arguments for tiff_path, output_path, overwrite, and verbose. For example,

`tiff2fits.convert("path/to/tiff.tiff", "my_converted_files", header=my_header, overwrite = True)`

Convert() returns the path to the saved FITS file.

Unlike the CLI, the python package is not designed for converting an entire directory. Rather, it converts individual files, passed via the tiff_path argument, and saves them to the output_path, which has the same rules as the CLI. If you wish to convert full directories in python, this is easily accomplished using [glob](https://docs.python.org/3/library/glob.html).

Working in python gives you the option to add headers to your converted FITS file by passing an [astropy.io.fits.Header](https://docs.astropy.org/en/latest/io/fits/api/headers.html#astropy.io.fits.Header) object.

&nbsp;
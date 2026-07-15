from PIL import Image
import numpy as np
from astropy.io import fits
from pathlib import Path
import argparse
from glob import glob

def convert(tif_path, output_path, header = None, overwrite: bool = False, verbose : bool = False, compress = True):
    '''
    Converts a Tag Image File Format (.tif) image to a FITS (.FTS) file.

    Arguments:
     tif_path: The path to the Tag Image File Format image you want to convert.
     output_path: The path to the file or directory you want to save the created FITS image in.
     headers (optional): astropy.io.fits.header.header() object to use as the header of the new FITS file.
    '''
    if verbose:
        print(f"Attempting to convert {tif_path}")
    with Image.open(tif_path) as img:
        img_name = Path(tif_path).stem
        img_array = np.array(img)
        img_mirror = np.flipud(img_array) #PIL loads upside down by default. Flipping gives original orientation.
        save_out_path = __get_save_out_path__(output_path=output_path, img_name=img_name)


        
        fits.HDUList([fits.PrimaryHDU(header=header, data=img_mirror if compress==False else None), _compress_(img_mirror, "RICE_1") if compress else None]).writeto(save_out_path, overwrite=overwrite)

        # if save_out_path:
        #     fits.writeto(save_out_path, compressed, header=header, overwrite=overwrite)
        #     if verbose:
        #         print(f"Saved conversion of {tif_path} as {save_out_path}")
        return f"{output_path}/{img_name}.FTS"
    
def _compress_(data : np.ndarray, algorithm : str):
    compressed = fits.CompImageHDU(data=data, compression_type=algorithm)
    return compressed


def __get_save_out_path__(output_path, img_name):

    output_path = Path(output_path)
    if not output_path.exists():
        output_path.touch()
    if Path(output_path).is_file():
        save_out_path = f"{output_path}"
    elif Path(output_path).is_dir():
        save_out_path = f"{output_path}/{img_name}.FTS"

    else:
        print("Not a usable output_path.")
    return save_out_path


    
    

def __get_args__():
    parser = argparse.ArgumentParser(
    prog='tif2FITS',
    description='Converts .tif files to .FTS files'

    )
    parser.add_argument('input_path')
    parser.add_argument('output_path')
    parser.add_argument('-o', '--overwrite', action='store_true')
    parser.add_argument('-y', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--compress', action=argparse.BooleanOptionalAction, default=True, help="Enable or disable FITS compression via RICE1 algorithm.")


    args = parser.parse_args()
    return args

def __try_convert__(file, op, args):
    try: 
        convert(file, op, header=None, overwrite=args.overwrite, verbose=args.verbose, compress=args.compress)
    except Exception as e:
        print(e)
    return

def main():
    args = __get_args__()

    ip = Path(args.input_path)
    op = Path(args.output_path)
    

    if ip.is_file():
        __try_convert__(ip, op, args=args)

    elif ip.is_dir():
        if not op.is_dir(): #Prevents writing over same file repeatedly. Unnecessary error if really only 1 file in directory to convert but in that case user should just pass file name.
            print("You passed a directory as your input so you must also pass an existing directory as your output.") #Existing because not including a file extension doesn't make a directory.
            return
        tif_file_list = glob(f"{ip}/*.tif")
        tif_file_list += glob(f"{ip}/*.tiff")
        for file in tif_file_list:
            __try_convert__(file=file, op=op, args=args)

    else:
        print("input_path was not valid.")

    return
        
    

if __name__ == "__main__":
    main()
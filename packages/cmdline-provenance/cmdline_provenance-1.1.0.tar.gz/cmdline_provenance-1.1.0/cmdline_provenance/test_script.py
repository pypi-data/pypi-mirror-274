'Print the input arguments to the screen.'

import argparse
import pdb

#import xarray as xr

import cmdline_provenance as cmdprov


def main(args):
    """Run the program."""

#    dset1 = xr.open_dataset(args.infile1)
#    dset2 = xr.open_dataset(args.infile2)
    new_log = cmdprov.new_log(
        infile_logs={'file.nc': 'file history...'},
        code_url='https://github.com/',
        extra_notes=['note1', 'note2'],
        wildcard_prefixes=[
            '/g/data/ob53/BARRA2/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/day/pr/v20231001/',
            '/g/data/ob53/BARRA2/output/reanalysis/AUS-11/BOM/ERA5/ssp370/hres/BARRA-R2/v1/day/pr/v20231001/',
        ]
    )
    print(new_log)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    
    parser.add_argument("infiles", type=str, nargs='*', help="Input file names")
    parser.add_argument("outfile", type=str, help="Output file name")
    parser.add_argument("--more_files", type=str, nargs='*', help="More input file names")

    args = parser.parse_args()            
    main(args)

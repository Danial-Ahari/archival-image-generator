# archival-image-generator
A very specific image generator created for use in an Archives in Special Collections

# Foreword
The status quo method used in the Archives and Special Collections that I work in utilized two original scans of each document (a 300 dpi "master" TIFF, and a 300 dpi "altered" JPEG). The JPEG was further edited into a 150 dpi, 1500 pixels on longest side "web" JPEG. These web JPEGs were then combined into "upload" PDFs. This process is complicated for documents that require certain editing (rotations, crops, etc.), but is highly automateable for the trivial case (no editing required). This project seeks to automate that work and increase potential productivity.

# Requirements
- Python (tested with Python 3.10)
- ImageMagick (tested with portable Windows 64 bit version)
- Windows (this should be relatively easily editable (changing shell commands) to run on POSIX systems though)

# How to use

## Starting the application
Once the pre-requisites are installed, it should be as simple as double-clicking the python script, so long as python is set up properly on the system.

## Supported major inputs
- TIFF "master" files
- JPEG "master" files
- JPEG "altered" files

## Intermediate files
- JPEG "altered" files
- JPEG "web" files

## Potential outputs
- JPEG "altered" files
- JPEG "web" files
- PDF "upload" files

## Input directories
Both input directories should contain the trailing \ at the end to indicate that it is a directory.

### ImageMagick
This should be the full path to where the ImageMagick executables (namely magick and identify) are located. If using the portable version, this is the folder within the folder resulting from unzipping the ZIP file.

### TIFF/JPEG files
This should be the full path to the parent directory containing "master", "altered", and "upload" (the latter two can be created by this program if not present). Alternately, select the checkbox below this text box and use a file pattern consisting of the parent directory followed by the start of the file name, e.g. abc_defg_000001 DO NOT use the full path to the files containing that file pattern (e.g. the master, altered, or upload directories).

File patterns are tested to work for TIFF inputs. JPEG inputs are untested, but should work.

## Input Type
Select the main type of file being input, if the main input is being utilized for the current operation (that is, if at least "altered" or "web" files are being generated).

## Output Resolution and Size

### DPI
This DPI value should be the DPI value that will be used for generating web copies (and in turn the PDFs). In our workflow, this is 150 DPI.

### Longest Side in Pixels
This value should be the number of pixels that you wish to be used for the longest side. For example, in our workflow, the longest side is 10 inches, and we export in 150 dpi, so the number of pixels is 10*150 or 1500.

## PDF File Name
If outputting a PDF, this text box will be used for the filename that will be exported into the "upload" directory, minus the extension.

## Generation Selections

### Generate "altered" JPEGs
These JPEGs are essentially just copies of the TIFFs with 100% quality and whatever DPI the TIFFs had.

### Generate "web" JPEGs
These JPEGs are scaled versions of the altered JPEGs, exported with 100% quality, and made to the resolution and longest side in pixels input above.

### Generate PDF (no OCR).
These PDFs are multi-page PDFs containing the web JPEGs that are in the directory (in directory mode) or match the file pattern (in file pattern mode).

## Further work
After generating this PDFs, one must use an external OCR engine to generate text.

# Example Workflow
Given: 39 TIFF files representing objects xxx_xxxx_749 to xxx_xxxx_765

1. Set up program to take TIFF files from directory containing those files. Change DPI and size settings to match web quality preferences.
2. Select Generate altered JPEGs and Generate web JPEGs
3. Click Generate files
4. Wait until it finished
5. Change the input directory to a file pattern <directory>/xxx_xxxx_749
6. Change PDF file name to xxx_xxxx_749
7. Deselect JPEG generation options and select Generate PDF (no OCR).
8. Click Generate files
9. Repeat steps 5 through 8 for each remaining object.
10. Open all PDFs in the "upload" directory in an external OCR engine and perform OCR on them.
11. All altered, web, and upload files are now created. Move them to appropriate directories.

# Future Plans
The below are features that may be added.
- ~~Generation that is able to treat JPEGs as "master" (low priority; added in 0.2.0)~~
- ~~Restructure input file structure to assume "master" is in a directory within the given directory (medium priority; added in 0.2.0)~~
- Make the interface look a little bit nicer (Tkinter is a bit of a limitation here) (low priority)
- Port it to the PythonMagick library, as opposed to using native ImageMagick (low priority)
- ~~Make it save most of the config to a config file for later loading, so one doesn't have to retype (medium priority; added in 0.2.1)~~
- Make a command line interface that can run from a default config file. (very low priority)

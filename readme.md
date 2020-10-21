A project to automatically generate previews for VRAS sessions. 
# Setup 
To install the python dependencies, simply run `pip install -r requirements.txt`. 
For other dependencies, follow the correct section depending on which OS.
## Windows
If you have [choco](https://chocolatey.org/) installed, you can run `choco install imagemagick` to automatically install it. 
Now you need to set an [environment variable]() named `IMAGEMAGICK_BINARY` to `magick.exe` located in your installation directory. If installed with choco, this will be a folder in your `Program Files` folder, example: `C:\Program Files\ImageMagick-7.0.10-Q16-HDRI`.
## Ubuntu
Run `sudo apt install libmagick++-dev` to install the dependencies needed on Ubuntu. 
# Usage 
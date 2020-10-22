A project to automatically generate previews for VRAS sessions. 
# Setup 
To install the python dependencies, simply run `pip install -r requirements.txt`. 
For other dependencies, follow the correct section depending on which OS.
## Windows
If you have [choco](https://chocolatey.org/) installed, you can run `choco install imagemagick` to automatically install it. 
Now you need to set an [environment variable]() named `IMAGEMAGICK_BINARY` to `magick.exe` located in your installation directory. If installed with choco, this will be a folder in your `Program Files` folder, example: `C:\Program Files\ImageMagick-7.0.10-Q16-HDRI`.
## Ubuntu
Run `sudo apt install libmagick++-dev` to install the dependencies needed on Ubuntu. 
You now need to change a policy to allow use of the library. Run `sudo vim /etc/ImageMagick-6/policy.xml`, find the line which says `<policy domain="path" rights="none" pattern="@*"/>`, and comment it out(you can do this by surrounding it with `<!--` and `-->`).
# Usage 
Put as many trailers as you want into a new folder named `Trailers`. Put 6 posters in JPG format in a new folder named `Posters`. 
Once you've done this, you can run `python main.py` to generate a trailer, output file will be in the folder `output` and will be named `final.mp4`.
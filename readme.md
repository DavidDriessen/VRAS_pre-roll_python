A project to automatically generate previews for VRAS sessions. 
# Setup 
To install the python dependencies, simply run `pip install -r requirements.txt`. 
For other dependencies, follow the correct section depending on which OS.
## Windows
If you have [choco](https://chocolatey.org/) installed, you can run `choco install imagemagick` to automatically install it. 
Now you need to set an [environment variable](http://www.dowdandassociates.com/blog/content/howto-set-an-environment-variable-in-windows-command-line-and-registry/) named `IMAGEMAGICK_BINARY` to `magick.exe` located in your installation directory. If installed with choco, this will be a folder in your `Program Files` folder, example: `C:\Program Files\ImageMagick-7.0.10-Q16-HDRI`.
## Ubuntu
Run `sudo apt install libmagick++-dev` to install the dependencies needed on Ubuntu. 
You now need to change a policy to allow use of the library. Run `sudo vim /etc/ImageMagick-6/policy.xml`, find the line which says `<policy domain="path" rights="none" pattern="@*"/>`, and comment it out(you can do this by surrounding it with `<!--` and `-->`).
# Usage 
Put as many trailers as you want into a new folder named `Trailers`. Put 6 or more posters in a new folder named `Posters`.\
Create a folder called `Session`, in this folder create folders for your sessions. Example folder structure:
```
Sessions/
├── Fate UBW
│   └── Fate UBW.jpg
├── Fullmetal Alchemist
│   └── FMAB.jpg
└── Seasonal Anime #4 [Fall]
    ├── Hypnosis Mic.jpg
    └── Taiso Samurai.jpg
```
Please use the same filenames for trailers and posters. Example: `jojo.png` & `jojo.mp4`

Once you have followed all these steps, just do `python main.py`. All rendered pre-rolls will go in the folder called `output`.
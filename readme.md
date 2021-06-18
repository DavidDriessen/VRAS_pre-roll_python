A project to automatically generate previews for VRAS sessions.

# Setup 
To install the python dependencies, simply run `pip install -r requirements.txt`. 
For other dependencies, follow the correct section depending on which OS.

## Docker (from registry, recommended)
Docker is the recommended way to setup this project, it makes installation and usage much easier.

Then to run the project, run
```bash
docker run -it --rm \
-v "$(pwd):/app/data" \
daviddual/vras_pre-roll
```
Add ```--h265``` to the and of the command to render with h265 encoder. 

## Docker (from source)
Docker is the recommended way to setup this project, it makes installation and usage much easier.

To setup docker, run the following commands:
```bash
git clone https://github.com/DavidDriessen/VRAS_pre-roll.git
cd VRAS_pre-roll
docker build -t vras_pre-roll .
```
Then to run the project, run
```bash
docker run -it --rm \
-v "/$(pwd)/Sessions/:/app/Sessions" \
-v "/$(pwd)/Posters/:/app/Posters" \
-v "/$(pwd)/Trailers/:/app/Trailers" \
-v "/$(pwd)/output/:/app/output" \
VRAS_pre-roll
```
Add ```--h265``` to the and of the command to render with h265 encoder. 

## Windows
If you have [choco](https://chocolatey.org/) installed, you can run `choco install imagemagick` to automatically install it. 
Now you need to set an [environment variable](http://www.dowdandassociates.com/blog/content/howto-set-an-environment-variable-in-windows-command-line-and-registry/) named `IMAGEMAGICK_BINARY` to `magick.exe` located in your installation directory. If installed with choco, this will be a folder in your `Program Files` folder, example: `C:\Program Files\ImageMagick-7.0.10-Q16-HDRI`.

## Ubuntu
Run `sudo apt install libmagick++-dev` to install the dependencies needed on Ubuntu. 
You now need to change a policy to allow use of the library. Run `sudo vim /etc/ImageMagick-6/policy.xml`, find the line which says `<policy domain="path" rights="none" pattern="@*"/>`, and comment it out(you can do this by surrounding it with `<!--` and `-->`).

# Usage 
On your first run of the program, it will create 3 folders named `output`, `Posters`, `Trailers` and `Sessions`. 
The folder `output` will be used for temporary files and the final pre-rolls. The folder `Posters` should be filled with 6 or more posters for the currently showing showcase. The folder `Trailers` can have as many trailers as you want, these are the trailers shown in the bottom right of the screen. The folder `Sessions` should contain folders for diffrent sessions, example folder structure for the folder `Sessions` is below.
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

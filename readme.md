A project to automatically generate previews for VRAS sessions. 
# Setup 
To install the python dependencies, simply run `pip install -r requirements.txt`. 
For other dependencies, follow the correct section depending on which OS.
## Windows
If you have [choco](https://chocolatey.org/) installed, you can run `choco install imagemagick`. 
## Ubuntu
Run `sudo apt install imagemagick` to install the dependencies needed on Ubuntu. 
# Usage 
To render a pre-roll for your session put posters of currently showing shows under `Posters` and trailer videos under `Trailers`.
They will be in alphabetical order.

Than just run `main.py` and the render video will be under `output`.

To rerender from a stage just remove that stage and rerun. Al stages before will be reused.

##Options
###-force
Rerender everything
###-big or bigTrailers
Play the trailers in fullscreen
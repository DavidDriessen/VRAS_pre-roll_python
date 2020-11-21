from splash import splash
from moviepy.editor import *
import subprocess

# Stage 1 generating still frame 
splash().save_frame('./output/posters.png')

# Stage 2 Overlaying trailers over still frame

# Stage 3 generating still frame with current session poster

# Stage 4 concatenating stage 2 + 3
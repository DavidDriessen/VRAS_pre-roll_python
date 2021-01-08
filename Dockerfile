FROM ubuntu:18.04

# Install deps
WORKDIR /app
RUN apt-get update && apt-get -y install libmagick++-6.q16-dev python3 python3-pip ffmpeg imagemagick

COPY . .
RUN pip3 install -r requirements.txt

# Remove policy
RUN pattern='<policy domain="path" rights="none" pattern="@*"/>' && replace='<!-- <policy domain="path" rights="none" pattern="@*"/> -->' && sed --expression 's@$pattern@$replace@g' /etc/ImageMagick-6/policy.xml > /etc/ImageMagick-6/policy.xml

CMD python3 main.py
FROM ubuntu:18.04

# Install deps
RUN apt-get update && apt-get -y install libmagick++-6.q16-dev python

# Remove policy
RUN pattern='<policy domain="path" rights="none" pattern="@*"/>' && replace='<!-- <policy domain="path" rights="none" pattern="@*"/> -->' && sed --expression 's@$pattern@$replace@g' /etc/ImageMagick-6/policy.xml

WORKDIR /app
COPY * ./

CMD python main.py
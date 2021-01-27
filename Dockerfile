FROM ubuntu:18.04

# Install deps
WORKDIR /app
RUN apt-get update && apt-get -y install python3 python3-pip ffmpeg
ADD ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD python3 main.py
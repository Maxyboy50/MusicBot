FROM ubuntu:22.04

ADD bot.py /app_files/
ADD requirements.txt /app_files/

USER root
RUN apt update && apt install -y python3.10 && apt install -y python3-pip && apt install -y ffmpeg
RUN ls /app_files/
RUN python3 -m pip install -r /app_files/requirements.txt

ENV MUSIC_BOT_TOKEN=$MUSIC_BOT_TOKEN


CMD [ "python3", "/app_files/bot.py" ]

FROM ubuntu:latest

WORKDIR /app_files

RUN apt install docker -y && apt install aws-cli

COPY dockerpublish.sh /app_files/scripts/

ENTRYPOINT ["/bin/bash"]


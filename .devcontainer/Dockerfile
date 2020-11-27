ARG VARIANT="14"
FROM mcr.microsoft.com/vscode/devcontainers/javascript-node:0-${VARIANT}

RUN apt-get update --fix-missing
RUN apt-get install -y python3-pip python3-opencv
RUN python3 -m pip install flake8

ARG VARIANT="14"
FROM mcr.microsoft.com/vscode/devcontainers/javascript-node:0-${VARIANT}

RUN apt-get update --fix-missing
RUN apt-get install -y python3-pip python3-opencv
RUN python3 -m pip install flake8

RUN wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz --no-check-certificate
RUN mkdir install-tl-unx
RUN tar -xf install-tl-unx.tar.gz -C install-tl-unx && rm install-tl-unx.tar.gz
RUN cd install-tl-unx/install-tl* && echo "selected_scheme scheme-basic" >> tex.profile && ./install-tl -profile tex.profile
ENV PATH="/usr/local/texlive/2021/bin/x86_64-linux:${PATH}"

RUN tlmgr install latexmk texliveonfly babel-german hyphen-german

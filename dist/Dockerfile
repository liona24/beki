FROM python:3.7-slim

RUN apt-get update -y --fix-missing && apt-get upgrade -y

RUN apt-get install -y --no-install-recommends nginx python3-dev build-essential python3-opencv wget

WORKDIR /tmp
RUN wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz --no-check-certificate
RUN mkdir install-tl-unx
RUN tar -xf install-tl-unx.tar.gz -C install-tl-unx && rm install-tl-unx.tar.gz
RUN cd install-tl-unx/install-tl* && \
    echo "selected_scheme scheme-basic" >> tex.profile && \
    ./install-tl -profile tex.profile
ENV PATH="/usr/local/texlive/2020/bin/x86_64-linux:${PATH}"
RUN tlmgr install latexmk

RUN mkdir -p /mnt/beki/

WORKDIR /www

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY bundle/tex ./tex
COPY tex_packages.txt .
RUN tlmgr install $(cat tex_packages.txt)

RUN apt-get remove -y wget
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

COPY bundle/static ./static

RUN useradd -p uwsgi uwsgi
COPY bundle/app /home/uwsgi/app
COPY settings.py /home/uwsgi/app/settings.py
RUN chown -R uwsgi:uwsgi /home/uwsgi/app

COPY uwsgi.ini .
COPY start.sh .
COPY nginx.conf /etc/nginx/nginx.conf

RUN chmod -R 644 /www
RUN chmod 100 start.sh

# For some reason this is not added to path causing opencv to not be found
ENV PYTHONPATH="${PYTHONPATH}:/usr/lib/python3/dist-packages"

EXPOSE 5000

CMD ["./start.sh"]

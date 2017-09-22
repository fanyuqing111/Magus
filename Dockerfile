FROM debian:testing

MAINTAINER Xero-Hige <Gaston.martinez.90@gmail.com>
WORKDIR /

RUN echo "deb http://mirrors.dcarsat.com.ar/debian/ testing main contrib non-free \
          \ndeb-src http://mirrors.dcarsat.com.ar/debian/ testing main contrib non-free" > /etc/apt/sources.list

RUN apt-get update && \
    apt-get install -y --no-install-recommends aptitude && \
    aptitude install -y \
        wget \
        locales \
        python3-pip \
		python3-setuptools && \
    rm -rf /var/lib/apt/lists/* && \
    aptitude clean

RUN pip3 install twitter --no-cache-dir && \
    pip3 install pika --no-cache-dir && \
    pip3 install Cython --no-cache-dir && \
    pip3 install word2vec --no-cache-dir

COPY /src /Magus
COPY /tweets /training

WORKDIR /Magus

CMD ["bash","StartMagus.sh"]

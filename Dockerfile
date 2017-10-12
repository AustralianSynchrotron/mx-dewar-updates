FROM python:3.5.1
RUN mkdir -p /srv/app
WORKDIR /srv/app
RUN apt-get update \
    && apt-get -y install libzbar-dev \
    && wget --quiet https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.3/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz -O /tmp/wkhtmltox.tar.xz \
    && echo "40bc014d0754ea44bb90e733f03e7c92862f7445ef581e3599ecc00711dddcaa /tmp/wkhtmltox.tar.xz" | sha256sum -c - && tar -xf /tmp/wkhtmltox.tar.xz -C /opt/ \
    && ln -s /opt/wkhtmltox/bin/* /usr/local/bin/ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
COPY requirements.txt /srv/app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /srv/app
RUN pip install --no-cache-dir -e .

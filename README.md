Flask app to email sample dewar updates.

## Installation

### CentOS 7

```bash
sudo yum install libjpeg-turbo-devel
wget http://download.gna.org/wkhtmltopdf/0.12/0.12.3/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz -O /tmp/wkhtmltox.tar.xz
echo "40bc014d0754ea44bb90e733f03e7c92862f7445ef581e3599ecc00711dddcaa /tmp/wkhtmltox.tar.xz" | sha256sum -c - && sudo tar -xf /tmp/wkhtmltox.tar.xz -C /opt/
sudo ln -s /opt/wkhtmltox/bin/* /usr/local/bin/
git clone https://github.com/AustralianSynchrotron/mx-dewar-updates.git
cd mx-dewar-updates
pip3 install .
```

## Development

wkhtmltopdf and zbar libraries are required for development. The
following commands will install them on Debian:

```
apt-get -y install libzbar-dev
wget http://download.gna.org/wkhtmltopdf/0.12/0.12.3/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz -O /tmp/wkhtmltox.tar.xz
echo "40bc014d0754ea44bb90e733f03e7c92862f7445ef581e3599ecc00711dddcaa /tmp/wkhtmltox.tar.xz" | sha256sum -c - && sudo tar -xf /tmp/wkhtmltox.tar.xz -C /opt/
sudo ln -s /opt/wkhtmltox/bin/* /usr/local/bin/
```

Once the above are installed you can clone the repository and install the
required packages in a virtual environment as follows:

```
git clone git@github.com:AustralianSynchrotron/mx-dewar-updates.git
cd mx-dewar-updates
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

You can then run the tests with `py.test`.

### With Docker

#### Build

```bash
docker build -t dewarupdates .
```

#### Test

```bash
docker run dewarupdates py.test
```

#### Run

Set the `PUCKTRACKER_URL` environment variable to the pucktracker-server http
api url (eg `http://192.168.1.1:8001`) and run:

```bash
docker run -p 5000:5000 --env PUCKTRACKER_URL dewarupdates ./manage.py runserver --host 0.0.0.0
```

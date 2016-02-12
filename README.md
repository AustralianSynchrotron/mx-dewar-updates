Flask app to email sample dewar updates

## Installation

### CentOS 7

```
sudo yum install libjpeg-turbo-devel
wget http://download.gna.org/wkhtmltopdf/0.12/0.12.3/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz -O /tmp/wkhtmltox.tar.xz
echo "40bc014d0754ea44bb90e733f03e7c92862f7445ef581e3599ecc00711dddcaa /tmp/wkhtmltox.tar.xz" | sha256sum -c - && sudo tar -xf /tmp/wkhtmltox.tar.xz -C /opt/
sudo ln -s /opt/wkhtmltox/bin/* /usr/local/bin/
git clone https://github.com/AustralianSynchrotron/mx-dewar-updates.git
cd mx-dewar-updates
pip3 install .
```

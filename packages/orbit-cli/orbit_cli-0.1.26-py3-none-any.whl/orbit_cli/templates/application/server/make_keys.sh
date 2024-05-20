#!/usr/bin/env bash

if [ ! -d "$1" ]; then
        echo "SSL configuration folder is missing"
        exit
fi
cd $1 2>/dev/null
if [ $? -ne 0 ]; then
        echo "Failed to CD to :: $1"
        exit
fi
if [ $2 ]; then
        hname="$2"
else
        hname="localhost"
fi

export EASYRSA_BATCH=1
export EASYRSA_REQ_EMAIL="demo@madpenguin.uk"
export EASYRSA_REQ_CN="${hname}"
export EASYRSA_REQ_OU="Community"
export EASYRSA_REQ_ORG="Madpenguin Consulting"
export EASYRSA_REQ_CITY="The Internet"
export EASYRSA_REQ_PROVINCE="The Web"
export EASYRSA_REQ_COUNTRY="UK"
export EASYRSA_KEY_SIZE="2048"
export EASYRSA_CERT_EXPIRE="90"
export EASYRSA_CRL_DAYS="3560"
export EASYRSA_DIGEST="sha512"

if [ ! -d "ca" ]; then
        echo "Creating a new CA in `pwd`"
        mkdir -p ca/easy-rsa ca/practice-csr
        chmod -Rv 700 ca
        cd ca/easy-rsa
        if [ -d /usr/share/easy-rsa ]; then
                ln -s /usr/share/easy-rsa/* .
        else
                ln -s /usr/local/etc/easy-rsa/* .
                ln -s /usr/local/bin/easyrsa .
                ln -s /usr/local/etc/pki .
        fi
        ./easyrsa init-pki
        ./easyrsa --days=3650 build-ca nopass
        cd ../..
fi

rm -f ca/easy-rsa/pki/private/localhost.key
rm -f ca/easy-rsa/pki/issued/localhost.crt
cd ca/easy-rsa

./easyrsa gen-req localhost nopass >/dev/null 2>&1
./easyrsa sign-req server localhost nopass >/dev/null 2>&1
cd ..
cp easy-rsa/pki/private/localhost.key .
cp easy-rsa/pki/issued/localhost.crt .
exit
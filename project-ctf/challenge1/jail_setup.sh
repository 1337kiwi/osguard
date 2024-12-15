#!/bin/bash

adduser --disabled-password --gecos "" -u 1001 ctfuser

chmod 700 /sbin/*

chmod 700 /usr/sbin/*

chmod 700 /usr/bin/*

chmod 711 /bin
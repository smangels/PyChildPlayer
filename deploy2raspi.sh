#!/bin/bash

# expect ENVIRONMENT variable RASPI_HOST
RASPI_HOSTNAME="childplayer"

rm -f *.pyc
scp *.py ${RASPI_HOSTNAME}:.




#!/bin/sh

black --line-length=100 protop2g/
isort --profile=black protop2g/
flake8 --max-line-length=100 protop2g/

#!/bin/bash

#brew install composer \
sudo apt-get install composer \
    && mkdir temp \
    && cd temp \
    && composer require istom1n/fpdi-tfpdf \
    && mv vendor/istom1n/fpdi-tfpdf ../fpdf \
    && cd .. \
    && rm -r temp


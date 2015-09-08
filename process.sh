#!/bin/bash

in2csv source-data/Dioceses6515states.xlsx --sheet 1965 > processed-data/1965.csv
in2csv source-data/Dioceses6515states.xlsx --sheet 2015 > processed-data/2015.csv

./process.py

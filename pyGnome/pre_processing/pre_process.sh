#!/bin/bash

source /home/andrea/anaconda3/bin/activate Python27
python /DATA/forecastData/scripts/hycomDownload.py
python /home/andrea/python/OilSpillForecastSystem/pyGnome/pre_processing/run_all.py

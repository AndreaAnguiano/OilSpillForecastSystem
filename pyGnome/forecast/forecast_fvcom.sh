#!/bin/bash

scp -P 23222 andrea@132.248.8.98:/DATA/forecastData/Currents_FVCOM/fvcom* /media/storageBK/Andrea/python/forecastData/Currents_FVCOM/
source /home/isabelanguiano/anaconda3/bin/activate Python27
python /media/storageBK/Andrea/python/OilSpillForecastSystem/pyGnome/forecast/runall_fvcom.py
~

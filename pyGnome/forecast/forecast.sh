#!/bin/bash

scp -P 23222 andrea@132.248.8.98:/DATA/forecastData/Currents/hycom* /media/storageBK/Andrea/python/forecastData/Currents/
scp -P 23222 andrea@132.248.8.98:/DATA/forecastData/Winds/* /media/storageBK/Andrea/python/forecastData/Winds/
source /home/isabelanguiano/anaconda3/bin/activate Python27
python /media/storageBK/Andrea/python/OilSpillForecastSystem/pyGnome/forecast/run_all.py
~  

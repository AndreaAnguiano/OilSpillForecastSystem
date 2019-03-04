
# Installation 

## 0. Creating an environment with python 2.7 

  > conda create -n Python27 python=2.7
  
  To activate an environment
  
  > source activate Python27
  
  To deactivate an environment 
  
  > source deactivate

## 1. Adding extra channels to conda

Add the NOAA-ORR-ERD channel 

> conda config --add channels NOAA-ORR-ERD

Add the conda-forge channel

> conda config --get channels


## 3. Cloning the PyGnome git repository

> git clone https://github.com/NOAA-ORR-ERD/PyGnome.git

## 2. Install dependencies 

> cd PyGnome

 edit conda_requirements.txt, change pacakges to >= rather than just =

 conda install -c anaconda netcdf4 
 conda install -c conda-forge pyshp 
 conda install -c conda-forge gridded 
 conda install -c conda-forge nbsphinx 
 
> conda install --file conda_requirements.txt

## 2.5 Install netCDF

> conda install netCDF4

> sudo apt-get install libhdf5-serial-dev

> sudo apt-get install libnetcdf-dev

## 3. The Oil library 

> git clone https://github.com/NOAA-ORR-ERD/OilLibrary.git

> cd OilLibrary/

 edit conda_requirements.txt, change pacakges to >= rather than just =

> conda install --file conda_requirements.txt

> python setup.py install

## 4. Build py_gnome

> cd ../py_gnome


> python setup.py develop




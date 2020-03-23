
# Installation 

## 0. Creating an environment with python 2.7 
```
conda create -n Python27 python=2.7
```  
  To activate an environment
```  
source activate Python27
```  
  To deactivate an environment 
```  
source deactivate
```

## 0.5 Install netCDF dev libraries

```
sudo apt-get install libhdf5-serial-dev
sudo apt-get install libnetcdf-dev
```

## 1. Adding extra channels to conda

Add the NOAA-ORR-ERD channel 
```
conda config --add channels NOAA-ORR-ERD
```
Add the conda-forge channel
```
conda config --add channels conda-forge
```

## 3. Cloning the PyGnome git repository

```
git clone https://github.com/NOAA-ORR-ERD/PyGnome.git
cd PyGnome
```
Edit `conda_requirements.txt`, change packages from = to >=
```
conda install --file conda_requirements.txt
```

## 4. Clone the OilLibrary
```
git clone https://github.com/NOAA-ORR-ERD/OilLibrary.git
 cd OilLibrary/
```
Edit `conda_requirements.txt`, change packages from = to >=
```
conda install --file conda_requirements.txt
python setup.py install
```
## 4. Build py_gnome
```
cd ../py_gnome
python setup.py develop
```
# Running the Examples
There are examples of different physical processes involved in the movement of particles in oil spills:
1) movement of particles by oceanic currents
2) movement of particles by winds
2) movement of particles by ocean currents and winds
4) Oil degradation due to weatherers

To run the examples it is necessary to edit the main file and add the desired model. The models are: only_Winds, only_Currents, CurrentsAndWinds and allWeatherers.
These examples and the main file are in the pyGnome folder.  

## PyCharm configuration

Add the folder `pyGnome` as a new project.

Add the `Python27` environment to PyCharm. Go to: File --> Settings and search for 'interpreter'. 
Then click the `gears` icon and `add`.

Select `Conda Environment` --> `Existing Environment` --> `Select your Python27 folder`


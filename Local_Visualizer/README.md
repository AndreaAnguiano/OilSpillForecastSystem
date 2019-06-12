# Oil spill visualizer

## Apache
We need to add CORS to the file `apache2.conf` by adding the following line:


```
sudo vi /etc/apache2/apache2.conf
    Header always set Access-Control-Allow-Origin "*" 
```

Then we need to enable headers with:
```
    sudo a2enmod headers
    service apache2 restart
```

The images should be at the images folder. 

TODO improve a lot this readme


## Code

### getImages
Is a simple webservice that returns the images in a Json format depending on the received date. The request are 
`SERVER/getImages?date='2019-01-01'`

### animations.js
Is the main JS file, here is the number of containers is defined and most of the logic.

### Animation.js
Is a class that is created for each 'animation container'. 

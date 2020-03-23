<html>
  <head>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css" integrity="sha384-/Y6pD6FV/Vv2HJnA6t+vslU6fwYXjCFtcEpHbNJ0lyAFsXTsjBbfaDjzALeQsN6M" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/themes/base/jquery-ui.css">
    <link rel="stylesheet" type="text/css" href="css/main.css">
    <link rel="stylesheet" type="text/css" href="css/menus.css">
    
    <title> Información del Pronóstico</title>
  </head>
  
  <body>
      <header role="banner">
          <div class="container">
              <div id="topheader">
                    <nav class="navbar navbar-default" role="navigation">
                        
                        <div class="navbar-header">
                            
                            <button class="navbar-toggle" type="button" data-toggle="collapse" data-target=".navbar-collapse">
                                <span class="icon-bar"></span>
                                <span class="icon-bar"></span>
                                <span class="icon-bar"></span>
                            </button>
                            <a class="navbar-brand" href="http://132.248.8.98:50530/index.php">
                                <img class="img-responsive" src="img/logo-pronostico.png" width=900>
                            </a>
                        </div>
                        </nav>
                        <div id="topmenuIcons" class="clearfix">
                            <div id="topmenu">
                                <ul class="nav menu">
                                    <li class="item-101 default">
                                        <a href="http://132.248.8.98:50530/index.php">Inicio</a>
                                    <li class="item-102 default">
                                        <a href="http://132.248.8.98:50530/Acerca.php">Acerca</a>
                                        <li class="item-103 default">
                                            <a href="http://132.248.8.98:50530/Informacion-del-pronostico.php">Información del Pronóstico</a>
                                        
                                        


                                </ul>
                            </div>
                        </div>
                        <div class="maincontent">
                            <div class="item-page" itemscope="" itemtype="https://schema.org/Article">
                                <meta itemprop="inLanguage" content="en-GB">
                                         <br>
                                    <p style="text-align:center;font-size=18;">
                                        <strong> Pronóstico de Derrames de Petróleo en el Golfo de México</strong>
                                    </p>
                                    <p style="text-align:justify;font-size=18;">
                                      El pronóstico de derrames de petróleo se realiza utilizando la librería PyGNOME, en su versión 0.9.
                                      Utiliza información de los campos de velocidad del viento y de las corrientes oceánicas superficiales para modelar el transporte del petróleo.
                                    </p>
                                    <p style="text-align:left;font-size=18;">
                                        <strong> PyGNOME</strong>
                                    </p>
                                    <p style="text-align:justify;font-size=18;">
                                        PyGNOME es un conjunto de utilidades desarrolladas en el lenguaje de programación Python para El Entorno de Modelado Operativo General de la NOAA (GNOME), 
                                        el cual está diseñado para modelar derrames de petróleo y otros materiales peligrosos en el entorno costero (Beegle-Krause, 2001). 
                                        Es fundamentalmente, un modelo para el seguimiento de partículas de tipo Lagrangiano: el petróleo u otra sustancia se representa como Elementos Lagrangianos (EL) o partículas,
                                        con su movimiento y propiedades rastreadas en el tiempo. 
                                        Una serie de «motores» (cualquier proceso físico que mueve las partículas) actúan sobre los EL y cada uno representa un proceso físico diferente.
                                    </p>
                                     <p style="text-align:left;font-size=18;">
                                        <strong> Datos utilizados </strong>
                                    </p>
                                    <p style="text-align:justify;font-size=18;">
                                        Los datos de los campos de velocidad del viento en superficie se obtienen del modelo atmosférico Weather Research and Forecasting (WRF)
                                    y los datos de las corrientes oceánicas superficiales se obtienen del pronóstico para el Golfo de México del modelo oceánico Hybrid Coordinate Ocean Model (HYCOM).
                                    <br>
                                    El modelo WRF que se utiliza es ejecutado por el grupo Interacción Océano Atmósfera (IOA) del Centro de Ciencias de la Atmósfera (CCA), de la UNAM.
                                    Este modelo corre de manera operativa y la visualización de estos datos está disponible en la página http://grupo-ioa.atmosfera.unam.mx/pronosticos/.
                                    Estos datos tienen una resolución temporal diaria y una resolución espacial de 15 km.
                                    <br> 
                                    Los datos de las corrientes oceánicas del modelo HYCOM se descargan del servidor de datos de la página web del consorcio, mediante un protocolo de transferencia de archivos (ftp),
                                    disponibles en la página: https://www.hycom.org/data/gomu0pt04/expt-90pt1m000. Estos datos tienen una resolución temporal diaria y una resolución espacial de 1/25°.


                                    </p>
                                    
                                    <p style="text-align:left;font-size=18;">
                                        <strong> Bibliografía consultada </strong>
                                    <ul>
                                        <li> Beegle-Krause, J. (2001) General noaa oil modeling environment (gnome): a new spill trajectory model. In International Oil Spill Conference, number 2, pages 865–871. American Petroleum Institute.</li>
                                    </ul>
                                        
                                    </p>

                                    
                                
                            </div>
                            
                        </div>
              </div>
          </div>
           
            
      </header>
        <div id="footer" class="clearfix">
                <div class="moduletable">
                    <div class="custom">
                        <p style="text-align: center;">
                            <br>
                            TODOS LOS DERECHOS RESERVADOS © 2020 Grupo Interacción Océano-Atmósfera.
                            <br>
                             Centro de Ciencias de la Atmósfera, UNAM. Circuito de la investigación Científica s/n, Ciudad Universitaria, Delegación Coyoacán, C.P. 04510, Ciudad de México
                        </p>
                        
                    </div>
                </div>
        </div>
  </<body>
</html>
  </body>
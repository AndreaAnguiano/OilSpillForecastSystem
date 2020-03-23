<html>
  <head>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css" integrity="sha384-/Y6pD6FV/Vv2HJnA6t+vslU6fwYXjCFtcEpHbNJ0lyAFsXTsjBbfaDjzALeQsN6M" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/themes/base/jquery-ui.css">
    <link rel="stylesheet" type="text/css" href="css/main.css">
    <link rel="stylesheet" type="text/css" href="css/menus.css">
  
    
    <title> Pronóstico de derrames de petróleo en el Golfo de México</title>
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
                    
                <div class="row">
                <h2 style="text-align: center; font-size: 20px;">
                    <br>
                    El pronóstico de derrames de Petróleo en el Golfo de México opera diariamente, simula el inicio de un derrame de petróleo en seis puntos dentro del Golfo de México con una duración de cuatro días.
                    <br>
                    <br>
                    Utiliza datos de los campos de viento del modelo Weather Research and Forecasting Model (WRF) y datos de las corrientes oceánicas 
                    del modelo Hybrid Coordinate Ocean Model (HYCOM).
                    
                </h2>

                </div>    
              </div>
          </div>
           
            
      </header>

	<div class="container-fluid red ">
		<div class="row justify-content-center">
			<div class="col-lg-3 col-md-6 col-sm-12  col-xs-12 ">
				<span class="mycenter">P1</span>
				<canvas id="p1_canvas" width="100%" ></canvas>
				<?php 
					$jsObj = 'obj_p1';//This name MUST be harcoded
					include 'animControls.php';
				?>
			</div>        
			<div class="col-lg-3 col-md-6 col-sm-12  col-xs-12 ">
				<span class="mycenter">P2</span>
				<canvas id="p2_canvas" width="100%" ></canvas>
				<?php 
					$jsObj = 'obj_p2';//This name MUST be harcoded
					include 'animControls.php';
				?>
			</div>        
			<div class="col-lg-3 col-md-6 col-sm-12  col-xs-12 ">
				<span class="mycenter">P3</span>
				<canvas id="p3_canvas" width="100%" ></canvas>
				<?php 
					$jsObj = 'obj_p3';//This name MUST be harcoded
					include 'animControls.php';
				?>
                        </div>
                </div>
                <div class="row justify-content-center">
			      
			<div class="col-lg-3 col-md-6 col-sm-12  col-xs-12 ">
				<span class="mycenter">P4</span>
				<canvas id="p4_canvas" width="100%" ></canvas>
				<?php 
					$jsObj = 'obj_p4';//This name MUST be harcoded
					include 'animControls.php';
				?>
			</div>        
                             
			<div class="col-lg-3 col-md-6 col-sm-12  col-xs-12 ">
				<span class="mycenter">P5</span>
				<canvas id="p5_canvas" width="100%" ></canvas>
				<?php 
					$jsObj = 'obj_p5';//This name MUST be harcoded
					include 'animControls.php';
				?>
			</div>        
			<div class="col-lg-3 col-md-6 col-sm-12  col-xs-12 ">
				<span class="mycenter">P6</span>
				<canvas id="p6_canvas" width="100%" ></canvas>
				<?php 
					$jsObj = 'obj_p6';//This name MUST be harcoded
					include 'animControls.php';
				?>
			</div>        
			       
		</div>
		<div class="row justify-content-center">
			<p>Date: <input type="text" id="datepicker"></p>
		</div>
               

        
		
	</div>
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

	<script src="https://code.jquery.com/jquery-1.12.4.js"></script>
	<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js" integrity="sha384-b/U6ypiBEHpOf/4+1nzFpr53nxSS+GLCkfwBdFNTxtclqqenISfwAzpKaMNFNmj4" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/js/bootstrap.min.js" integrity="sha384-h0AbiXch4ZDo7tp9hKZ4TsHbi047NrKGLO3SEJAg45jXxnGIfYzk4Si90RDIqNm1" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/5.9.2/d3.min.js"></script>



		
    <script > var img_names= <?php echo json_encode($img_names); ?>;</script>
    <script > 
		//		console.log(img_names);
		//		console.log(last_image);
	</script>
    <script src="js/Tools.js"></script>
    <script src="js/Animation.js"></script>
    <script src="js/animations.js"></script>
  </body>
</html>
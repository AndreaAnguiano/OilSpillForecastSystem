<html>
  <head>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css" integrity="sha384-/Y6pD6FV/Vv2HJnA6t+vslU6fwYXjCFtcEpHbNJ0lyAFsXTsjBbfaDjzALeQsN6M" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/themes/base/jquery-ui.css">
    <link rel="stylesheet" href="css/main.css">
  </head>
  
  <body>
  
	<div class="container-fluid red ">
		<div class="row">
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
			<div class="col-lg-3 col-md-6 col-sm-12  col-xs-12 ">
				<span class="mycenter">P7</span>
				<canvas id="p7_canvas" width="100%" ></canvas>
				<?php 
					$jsObj = 'obj_p7';//This name MUST be harcoded
					include 'animControls.php';
				?>
			</div>        
		</div>
		<div class="row">
			<p>Date: <input type="text" id="datepicker"></p>
		</div>

    <footer class="footer">
      <div class="d-flex justify-content-end" style="height: 65px;">

		  <p class="mr-auto p-2"><a href='http://olmozavala.com'>Olmo Zavala</a>,
			  Adolfo V. Magaldi,
			  Angel Ruiz, 
			  Carlos Ochoa,
			  A. Quintanar,
			  Michel Grutter,
			  Eugenia González,
			  <a href="https://github.com/ixchelzg">Ixchel Zazueta</a>, 2019
		  </p>
			  <img src="img/unam.png" class="nav_logo_min"  />
			  <img src="img/logo.png" class="nav_logo_min"  />
	  </div>
		  
    </footer>
		
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
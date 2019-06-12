<?php
# Required format for date is YYYY-MM-DD
$currDate= $path . $_GET['date'];

if(empty($currDate)){
	$currDate = date('Y-m-d');
}

$tot_points = 7;

$array_all_imgs = [];
for ($i = 1; $i <= $tot_points; $i++) {
	$currFolder = "images/" . $currDate . "/P".$i."/";
	$img_names = glob($currFolder. "*.png");
//	array_push($array_all_imgs,$img_names);
	$array_all_imgs["P".$i] = $img_names;
}
//print_r($array_all_imgs);

header('Content-type: application/json');
echo json_encode($array_all_imgs);
?>
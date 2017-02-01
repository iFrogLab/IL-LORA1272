<?php

if(!defined('INCLUDE_CHECK')) die('You are not allowed to execute this file directly');

 
$db_host		= 'localhost';
$db_user		= 'ifroglab';
$db_pass		= 'ifroglab';
$db_database	= 'ifroglab'; 

	//Open database connection
//	$con = mysql_connect("localhost","root","");
//	mysql_select_db("db449462569", $con);
	



 
	$link =$con = po_mysql_connect($db_host,$db_user,$db_pass,$db_database);

	



 


/* 程式上傳後需要修改的地方  */
$title='iFrogLab ICBlock';
$email	= 'support@looptek.com'; 
$website = 'http://www.ifroglab.com';
$tableGroup = 'groupTable';
$tablepeople= 'people';
$tabledeviceHistory='deviceHistory';
$IoTTable='IoTTable';
$IoTProjects='IoTProjects';



?>

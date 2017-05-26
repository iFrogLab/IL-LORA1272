<?php

if(!defined('INCLUDE_CHECK')) die('You are not allowed to execute this file directly');

 
$db_host		= 'localhost';
$db_user		= 'root';
$db_pass		= 'ntunhs';
$db_database	= 'iot'; 

$link =$con = po_mysqli_connect($db_host,$db_user,$db_pass,$db_database);

	
/* 程式上傳後需要修改的地方  */
$title='iFrogLab ICBlock';
$email	= 'support@looptek.com'; 
$website = 'http://www.ifroglab.com';
$tableGroup = 'groupTable';
$tablepeople= 'people';
$tabledeviceHistory='deviceHistory';
$IoTTable='iottable';
$IoTProjects='IoTProjects';



?>

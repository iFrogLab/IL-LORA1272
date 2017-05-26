<?php

if(!defined('INCLUDE_CHECK')) die('You are not allowed to execute this file directly');

function checkEmail($str)
{
	return preg_match("/^[\.A-z0-9_\-\+]+[@][A-z0-9_\-]+([.][A-z0-9_\-]+)+[A-z]{1,4}$/", $str);
}


function send_mail($from,$to,$subject,$body)
{
	$headers = '';
	$headers .= "From: $from\n";
	$headers .= "Reply-to: $from\n";
	$headers .= "Return-Path: $from\n";
	$headers .= "Message-ID: <" . md5(uniqid(time())) . "@" . $_SERVER['SERVER_NAME'] . ">\n";
	$headers .= "MIME-Version: 1.0\n";
	$headers .= "Date: " . date('r', time()) . "\n";

	mail($to,$subject,$body,$headers);
}
function po_mysql_close($con){
	if (version_compare(PHP_VERSION, '4.1.13') >= 0) {
		mysqli_close($con);
	}else{
		mysql_close($con);
	}
}
function po_mysqli_connect($db_host,$db_user,$db_pass,$db_database)
{
	if (version_compare(PHP_VERSION, '4.1.13') >= 0) {
		return mysqli_connect($db_host,$db_user,$db_pass,$db_database);
	}else{
		$con= mysql_connect($db_host,$db_user,$db_pass);
		mysql_select_db($db_database, $con);
        return $con;
	}
}

function po_mysqli_select_db($db_database, $con){
	/*
	if (version_compare(PHP_VERSION, '7.0.0') >= 0) {
		//return mysqli_select_db($db_database, $con);
	}else{
		return mysql_select_db($db_database, $con);
	}*/
}


function po_mysql_query($con,$sql){
	if (version_compare(PHP_VERSION, '4.1.13') >= 0) {
		return mysqli_query($con,$sql);
	}else{
		return mysql_query($sql);
	}
}

function po_mysql_fetch_array($con,$i1){
	if (version_compare(PHP_VERSION, '4.1.13') >= 0) {
		return mysqli_fetch_array($i1,MYSQLI_ASSOC);
	}else{
		return mysql_fetch_array($i1);
	}
}
 


function po_mysql_num_fields($con,$sql){
	if (version_compare(PHP_VERSION, '4.1.13') >= 0) {
		//return mysqli_num_fields($sql);
        return mysqli_num_fields($sql);
	}else{
		return mysql_num_fields($sql);
	}
}
function mysqli_field_name($result, $field_offset)
{
    $properties = mysqli_fetch_field_direct($result, $field_offset);
    return is_object($properties) ? $properties->name : null;
}

function po_mysql_field_name($sql,$i2){
	if (version_compare(PHP_VERSION, '4.1.13') >= 0) {
		# return mysqli_field_name($sql,$i2);
        return mysqli_field_name($sql,$i2);
	}else{
		return mysql_field_name($sql,$i2);
	}
}



















?>
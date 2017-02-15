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
	if (version_compare(PHP_VERSION, '7.0.0') >= 0) {
		mysqli_close($con);
	}else{
		mysql_close($con);
	}
}
function po_mysqli_connect($db_host,$db_user,$db_pass,$db_database)
{
	if (version_compare(PHP_VERSION, '7.0.0') >= 0) {
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


function po_mysql_query($sql){
	if (version_compare(PHP_VERSION, '7.0.0') >= 0) {
		return mysql_query($sql);
	}else{
		return mysql_query($sql);
	}
}

function po_mysql_fetch_array($i1){
	if (version_compare(PHP_VERSION, '7.0.0') >= 0) {
		return mysql_fetch_array($i1);
	}else{
		return mysql_fetch_array($i1);
	}
}
 


function po_mysql_num_fields($sql){
	if (version_compare(PHP_VERSION, '7.0.0') >= 0) {
		return mysqli_num_fields($sql);
	}else{
		return mysql_num_fields($sql);
	}
}

function po_mysql_field_name($sql,$i2){
	if (version_compare(PHP_VERSION, '7.0.0') >= 0) {
		return mysqli_field_name($sql,$i2);
	}else{
		return mysql_field_name($sql,$i2);
	}
}
















?>
<?php

define('INCLUDE_CHECK',true);

require 'functions.php';
require 'connect.php';

try
{
 //mysql_error(); 

	//Getting records (listAction)  
	if($_GET["action"] == "list")
	{
	    //Get record count
		$result = po_mysql_query($con,"SELECT COUNT(*) AS RecordCount FROM ".$IoTTable.";");
		$row = po_mysql_fetch_array($con,$result);
		$recordCount = $row['RecordCount'];

		//Get records from database
		$result = po_mysql_query($con,"SELECT * FROM ".$IoTTable." ORDER by Id DESC;");
		//$result = mysql_query("SELECT * FROM wp_users;");
		//$columns = po_mysql_num_fields($result); 
		
		/*
		$columns_name = array();
		for($i = 0; $i < $columns; $i++) { 
  			 $fieldName = po_mysql_field_name($result,$i);		
		  	 $columns_name[$i] = $fieldName;
		}
		*/
		//Add all records to an array
		$rows = array();
		while($row = po_mysql_fetch_array($con,$result))
		{
		    $rows[] = $row;
			////////
				if(isset($_GET['print'])) {
		  		   if($_GET["print"]=="no"){
  						$t_data =array();
						for($i = 0; $i < $columns; $i++) { 
							$t_data[$columns_name[$i]]=$row[$i] ;
						}
    					array_push($m_data, $t_data);
			 		}
				}
		}

		//Return result to jTable
		$jTableResult = array();
		$jTableResult['Result'] = "OK";
		$jTableResult['TotalRecordCount'] = $recordCount;
		$jTableResult['Records'] = $rows;
		
		if(isset($_GET['print'])) {
		     if($_GET["print"]=="no"){
			 }
		}else{
		
			print json_encode($jTableResult);
		}
		
		
	
	}
	// http://localhost/ICBlock/web/AjaxIoT.php?action=insertByAPIKey&KeyName=y&Data=3&Datatype=1&APIKey=iloveifroglab
	else if($_GET["action"] == "insertByAPIKey")
	{

		$jTableResult = array();
		$APIKey="iloveifroglab";
		if($APIKey==$_GET["APIKey"]){
			# 查出來的資料代號
			$OwnerId=0;
			$IoTProjectsId=0; //$_GET["IoTProjectsId"]=


			//# 保留最後50 筆資料
		    //$sql2="DELETE FROM ".$IoTTable."  WHERE id IN (SELECT id FROM ".$IoTTable."  where OwnerId=". $_GET["OwnerId"] ." ORDER BY id ASC LIMIT 5)";
		    //$sql2="DELETE FROM ".$IoTTable." WHERE Datetime IS NOT NULL order by Datetime ASC LIMIT 1";
	        $sql2="DELETE FROM ".$IoTTable." WHERE id <= ( SELECT id  FROM (     SELECT id     FROM ".$IoTTable."  WHERE OwnerId=". $OwnerId ." AND IoTProjectsId=".$IoTProjectsId." ORDER BY id DESC  LIMIT 1 OFFSET 50     ) foo )";
			$result = po_mysql_query($con,$sql2);

			$now = new DateTime();
		    $mysqltime = $now->format('Y-m-d H:i:s'); 
			//$sqldetet = "DELETE FROM  ".$IoTTable." WHERE id IN (SELECT id FROM  ".$IoTTable." ORDER BY id ASC LIMIT 100)";
			$sql="INSERT INTO ".$IoTTable."( KeyName,Data,OwnerId,Datatype,IoTProjectsId, Datetime) VALUES('" .
				   $_GET["KeyName"] . 
			 "','" . $_GET["Data"] .
			 "'," . $OwnerId .
			 "," . $_GET["Datatype"] .
			 ",".	$IoTProjectsId .
			 ",'".$mysqltime."');";
			$result1 = po_mysql_query($con,$sql); 

			$jTableResult = array();
			$jTableResult['Debug'] = $sql;
			
			$jTableResult['Result'] = "OK";
			$jTableResult['Record'] = $sql2;
		}else{
			$jTableResult['Result'] = "ERROR";
		}
		print json_encode($jTableResult);
	}	

	// http://localhost/ICBlock/web/AjaxIoT.php?action=insert&KeyName=x&Data=360&OwnerId=1&Datatype=1&IoTProjectsId=0
	else if($_GET["action"] == "insert")
	{
		//Insert record into database
		// $result = mysql_query("INSERT INTO people(Name, BirthDate,idNumber, RecordDate) VALUES('" . $_POST["Name"] . "', " . $_POST["BirthDate"] . ",'" . $_POST["idNumber"] . "',now());");


		# 保留最後50 筆資料
	    $sql2="DELETE FROM ".$IoTTable."  WHERE id IN (SELECT id FROM ".$IoTTable."  where OwnerId=". $_GET["OwnerId"] ." ORDER BY id ASC LIMIT 5)";
	    $sql2="DELETE FROM ".$IoTTable." WHERE Datetime IS NOT NULL order by Datetime ASC LIMIT 1";
        $sql2="DELETE FROM ".$IoTTable." WHERE id <= ( SELECT id  FROM (     SELECT id     FROM ".$IoTTable."  WHERE IoTProjectsId=". $_GET["OwnerId"] ."  AND  OwnerId=". $_GET["OwnerId"] ."  ORDER BY id DESC  LIMIT 1 OFFSET 50     ) foo )";
		$result = po_mysql_query($con,$sql2);


		$now = new DateTime();
	    $mysqltime = $now->format('Y-m-d H:i:s'); 
		//$sqldetet = "DELETE FROM  ".$IoTTable." WHERE id IN (SELECT id FROM  ".$IoTTable." ORDER BY id ASC LIMIT 100)";
		$sql="INSERT INTO ".$IoTTable."( KeyName,Data,OwnerId,Datatype, IoTProjectsId,Datetime) VALUES('" .
			   $_GET["KeyName"] . 
		 "','" . $_GET["Data"] .
		 "'," . $_GET["OwnerId"] .
		 "," . $_GET["Datatype"] . 
		",".	 $_GET["IoTProjectsId"] .
		 ",'".$mysqltime."');";
		$result1 = po_mysql_query($con,$sql); 

		$jTableResult = array();
		$jTableResult['Debug'] = $sql;

		$jTableResult['Result'] = "OK";
		$jTableResult['Record'] = $sql2;
		print json_encode($jTableResult);
	}	
	//Creating a new record (createAction)
	else if($_GET["action"] == "create")
	{
		//Insert record into database
		// $result = mysql_query("INSERT INTO people(Name, BirthDate,idNumber, RecordDate) VALUES('" . $_POST["Name"] . "', " . $_POST["BirthDate"] . ",'" . $_POST["idNumber"] . "',now());");

		$now = new DateTime();
	    $mysqltime = $now->format('Y-m-d H:i:s');


		$sql="INSERT INTO ".$IoTTable."( Data,OwnerId,Datatype,IoTProjectsId, Datetime) VALUES(" .
			   $_POST["Data"] . 
		 "," . $_POST["OwnerId"] .
		 "," . $_POST["Datatype"] .
		 "," . $_POST["IoTProjectsId"] .
		 ",'".$mysqltime."');";
		$result1 = po_mysql_query($sql);
		 
        //INSERT INTO IoTTable( Data,OwnerId,Datatype, Datetime) VALUES(,1,,0,now());


		
		
		//Get last inserted record (to return to jTable)
		$result = po_mysql_query("SELECT * FROM ".$IoTTable." ");
		$row = po_mysql_fetch_array($result);

		//Return result to jTable
		$jTableResult = array();
		$jTableResult['Debug'] = $sql;
		$jTableResult['Result'] = "OK";
		$jTableResult['Record'] = $row;
		print json_encode($jTableResult);
	}	
	//Updating a record (updateAction)
	
	else if($_GET["action"] == "update")
	{
		//Update record in database
		$sql="UPDATE ".$IoTTable." SET Datetime = '" . $_POST["Datetime"] . 
		                                    "', Data = " .$_POST["Data"] .
		                                    ", OwnerId = " .$_POST["Datatype"] .
										    ", Datatype = " .$_POST["Datatype"] .
		 								    ", IoTProjectsId = " .$_POST["IoTProjectsId"] .
										    " WHERE Id = " . $_POST["Id"] . ";";
		$result = po_mysql_query($sql);
		//Return result to jTable
		$jTableResult = array();
		$jTableResult['Debug'] =$sql;
		$jTableResult['Result'] = "OK";
		print json_encode($jTableResult);
	}
	//Deleting a record (deleteAction)
	else if($_GET["action"] == "delete")
	{
		//Delete from database
		$result = po_mysql_query("DELETE FROM ".$IoTTable." WHERE Id = " . $_POST["Id"] . ";");

		//Return result to jTable
		$jTableResult = array();
		$jTableResult['Result'] = "OK";
		print json_encode($jTableResult);
	}

	//Close database connection
	po_mysql_close($con);

}
catch(Exception $ex)
{
    //Return error message
	$jTableResult = array();
	$jTableResult['Result'] = "ERROR";
	$jTableResult['Message'] = $ex->getMessage();
	print json_encode($jTableResult);
}
	
?>
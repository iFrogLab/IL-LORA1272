<?php
$servername = "localhost";
$username = "root";
$password = "ntunhs";
$dbname = "iot";




// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$sql = "SELECT Id, Data  FROM iottable";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "id: " . $row["Id"]. " - Data: " . $row["Data"]. "<br>";
    }
} else {
    echo "0 results";
}
$conn->close();
?>
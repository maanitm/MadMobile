<?php
    include 'mysqlConnector.php';
    error_reporting(0);
    $conn = connect_to_mysql();

    $status = "ok";
    $message = "";

    // Define a 32-byte (64 character) hexadecimal encryption key
    // Note: The same encryption key used to encrypt the data must be used to decrypt the data
    define('ENCRYPTION_KEY', '59fccce55b22993129a7bc4dbc61a42c358a29aed0481b19669dbfd4cd97b6df');

    $sql = "SELECT * FROM liveData";

    $result = $conn->query($sql);

    $response = array();

    if ($result->num_rows > 0) {
        // output data of each row
        while ($row = mysql_fetch_array($result)) {
            // temp user array
            $liveData = array();
            $liveData["value"] = $row["value"];
            $liveData["type"] = $row["type"];
            $liveData["date"] = $row["date"];

            // push single product into final response array
            array_push($response, $liveData);
        }
        $status = "ok";
        $message = "data found";
    } else {
        $status = "ok";
        $message = "no data found";
    }

    $returnMessage = array("status" => $status, "message" => $message, "data" => $response);

    header('Content-Type: application/json');
    echo json_encode($returnMessage);

    $conn->close();
?>

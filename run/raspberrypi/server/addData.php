<?php
    error_reporting(0);
    include 'mysqlConnector.php';

    $conn = connect_to_mysql();

    // Define a 32-byte (64 character) hexadecimal encryption key
    // Note: The same encryption key used to encrypt the data must be used to decrypt the data
    define('ENCRYPTION_KEY', '59fccce55b22993129a7bc4dbc61a42c358a29aed0481b19669dbfd4cd97b6df');

    $status = "ok";
    $message = "";

    $value = $_GET['value'];
    $type = $_GET['type'];
    $date = date('Y-m-d H:i:s');

    check_if_empty($_GET['value']);
    check_if_empty($_GET['type']);

    $sql = "INSERT INTO liveData (value, type, date) VALUES ('" . $value . "', '" . $type . "', '" . $date . "')";

    if ($conn->query($sql) === TRUE) {
        //
        $status = "ok";
        $message = "successfully added data";
    } else {
        $status = "error";
        $message = $conn->error;
    }

    $returnMessage = array("status" => $status, "message" => $message);

    header('Content-Type: application/json');
    echo json_encode($returnMessage);;

    $conn->close();
?>

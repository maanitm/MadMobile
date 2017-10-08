<?php
    include 'mysqlConnector.php';
    error_reporting(0);
    $conn = connect_to_mysql();

    $status = "ok";
    $message = "";

    // Define a 32-byte (64 character) hexadecimal encryption key
    // Note: The same encryption key used to encrypt the data must be used to decrypt the data
    define('ENCRYPTION_KEY', '59fccce55b22993129a7bc4dbc61a42c358a29aed0481b19669dbfd4cd97b6df');

    $api_key = $_POST['key'];
    
    authenticate_key($api_key, $conn);

    $sql = "SELECT * FROM categories";

    $result = $conn->query($sql);

    $categories = array();
    
    if ($result->num_rows > 0) {
        // output data of each row
        while($row = $result->fetch_assoc()) {
            $status = "ok";
            $message = "categories found";
            $categories[$row['category']] = $row['color'];
        }
    } else {
        $status = "ok";
        $message = "no categories found";
    }

    $returnMessage = array("status" => $status, "message" => $message, "categories" => $categories);
    
    header('Content-Type: application/json');
    echo json_encode($returnMessage);

    $conn->close();
?>

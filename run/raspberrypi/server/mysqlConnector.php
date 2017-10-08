<?php
    error_reporting(0);

    // Define a 32-byte (64 character) hexadecimal encryption key
    // Note: The same encryption key used to encrypt the data must be used to decrypt the data
    define('ENCRYPTION_KEY', '59fccce55b22993129a7bc4dbc61a42c358a29aed0481b19669dbfd4cd97b6df');
    // Encrypt Function
    function mc_encrypt($encrypt, $key){
        $encrypt = serialize($encrypt);
        $iv = mcrypt_create_iv(mcrypt_get_iv_size(MCRYPT_RIJNDAEL_256, MCRYPT_MODE_CBC), MCRYPT_DEV_URANDOM);
        $key = pack('H*', $key);
        $mac = hash_hmac('sha256', $encrypt, substr(bin2hex($key), -32));
        $passcrypt = mcrypt_encrypt(MCRYPT_RIJNDAEL_256, $key, $encrypt.$mac, MCRYPT_MODE_CBC, $iv);
        $encoded = base64_encode($passcrypt).'|'.base64_encode($iv);
        return $encoded;
    }
    // Decrypt Function
    function mc_decrypt($decrypt, $key){
        $decrypt = explode('|', $decrypt.'|');
        $decoded = base64_decode($decrypt[0]);
        $iv = base64_decode($decrypt[1]);
        if(strlen($iv)!==mcrypt_get_iv_size(MCRYPT_RIJNDAEL_256, MCRYPT_MODE_CBC)){ return false; }
        $key = pack('H*', $key);
        $decrypted = trim(mcrypt_decrypt(MCRYPT_RIJNDAEL_256, $key, $decoded, MCRYPT_MODE_CBC, $iv));
        $mac = substr($decrypted, -64);
        $decrypted = substr($decrypted, 0, -64);
        $calcmac = hash_hmac('sha256', $decrypted, substr(bin2hex($key), -32));
        if($calcmac!==$mac){ return false; }
        $decrypted = unserialize($decrypted);
        return $decrypted;
    }

    function connect_to_mysql() {
        $servername = "localhost";
        $username = "admin";
        $password = "madmobile1234";
        $dbname = "madmobile";

        // Create connection
        $conn = new mysqli($servername, $username, $password, $dbname);
        // Check connection
        if ($conn->connect_error) {
           die("Connection failed: " . $conn->connect_error);
        }

        return $conn;
    }

    function authenticate_key($api_key, $conn) {
        $sql = "SELECT * FROM api";
        $result = $conn->query($sql);

        $keyRetrieved = "";

        if ($result->num_rows > 0) {
            // output data of each row
            while($row = $result->fetch_assoc()) {
                $keyRetrieved = $row["api_key"];
            }

            $isKeyCorrect = password_verify($api_key, $keyRetrieved);

            if ($isKeyCorrect) {
                $status = "ok";
                $message = "correct api key";
            }
            else {
                $status = "error";
                $message = "incorrect api key";
                $returnMessage = array("status" => $status, "message" => $message);
                header('Content-Type: application/json');
                exit(json_encode($returnMessage));
            }
        } else {
            $status = "error";
            $message = "could not access database";
            $returnMessage = array("status" => $status, "message" => $message);
            header('Content-Type: application/json');
            exit(json_encode($returnMessage));
        }
    }

    function check_if_empty($var) {
        if (empty($var)) {
            $status = "error";
            $message = "missing parameter";
            $returnMessage = array("status" => $status, "message" => $message);
            header('Content-Type: application/json');
            exit(json_encode($returnMessage));
        }
    }

    function Encrypt($password, $data) {
        $salt = substr(md5(mt_rand(), true), 8);

        $key = md5($password . $salt, true);
        $iv  = md5($key . $password . $salt, true);

        $ct = mcrypt_encrypt(MCRYPT_RIJNDAEL_128, $key, $data, MCRYPT_MODE_CBC, $iv);

        return base64_encode('Salted__' . $salt . $ct);
    }
    function Decrypt($password, $data) {
        $data = base64_decode($data);
        $salt = substr($data, 8, 8);
        $ct   = substr($data, 16);

        $key = md5($password . $salt, true);
        $iv  = md5($key . $password . $salt, true);

        $pt = mcrypt_decrypt(MCRYPT_RIJNDAEL_128, $key, $ct, MCRYPT_MODE_CBC, $iv);

        return $pt;
    }
?>

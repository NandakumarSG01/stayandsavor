<?php
$servername = "localhost";
$username = "root";
$password = "PHW#84#jeor";
$dbname = "staysavor";

// Create a connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check the connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Ensure that these keys exist in the POST request
    $user = isset($_POST["username"]) ? $_POST["username"] : "";
    $email = isset($_POST["email"]) ? $_POST["email"] : "";
    $pass = isset($_POST["password"]) ? $_POST["password"] : "";

    // Insert data into the registerinfo table
    $sql = "INSERT INTO registerinfo (username, email, password) VALUES ('$user', '$email', '$pass')";

    if ($conn->query($sql) === TRUE) {
        echo "Registration successful!";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
}

$conn->close();
?>

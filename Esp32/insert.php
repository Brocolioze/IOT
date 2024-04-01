<?php
$data = file_get_contents('php://input');
$json_data = json_decode($data, true);

$latitude = $json_data['latitude'];
$longitude = $json_data['longitude'];
$servername = "localhost"; 
$username = "anthony"; 
$password = "Gatineau50."; 
$dbname = "BDAlawan"; 

try {
    $dsn = "mysql:host=$servername;dbname=$dbname";
    $pdo = new PDO($dsn, $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);


    if ($latitude !== null && $longitude !== null) {
        $sql = "INSERT INTO GPSData (latitude, longitude) VALUES (?, ?)";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$latitude, $longitude]);

        echo $latitude;
        echo $longitude;
        echo "Données GPS insérées avec succès dans la base de données";
    } else {
        echo "Erreur: Latitude ou longitude manquante.";
    }

} catch (PDOException $e) {
    echo "Erreur lors de l'insertion des données GPS: " . $e->getMessage();
}
?>

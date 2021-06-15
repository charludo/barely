<?php
    $servername = "rdbms.strato.de";
    $username = "U3162331";
    $password = "t9BSpUrsdKGT4LhV";

    // Only process POST reqeusts.
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $stellen = $_POST["stellen"];

        $pdo = new PDO('mysql:host=rdbms.strato.de;dbname=DB3162331;charset=utf8', $username, $password);
        $sql = "UPDATE stellenBaumgartner SET stellen='$stellen'";
        $pdo->exec($sql);

        echo "<html>
        <head>
        <meta charset='utf8'>
        </head>
        <body>Die Stellenanzeigen wurden aktualisiert.<br />
        <a href='index.php'>Zurück zur Verwaltung</a></body>
        </html>";
    };
?>

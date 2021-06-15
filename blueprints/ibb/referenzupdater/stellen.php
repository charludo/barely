<html>

    <head>
        <meta charset="utf8">
        <title>Stellenanzeigen</title>
        <link rel="stylesheet" type="text/css" href="styleupdater.css"/>
    </head>

    <body>
        <div class="contentContainer">
        <?php
            $servername = "rdbms.strato.de";
            $username = "U3162331";
            $password = "t9BSpUrsdKGT4LhV";
            $pdo = new PDO('mysql:host=rdbms.strato.de;dbname=DB3162331;charset=utf8', $username, $password);
            $sql = $pdo->prepare("SELECT stellen FROM stellenBaumgartner");
            $sql->execute();
            $row = $sql->fetch();
            $stellen = $row["stellen"];
                echo'<form method="post" action="updatestellen.php">

                    <textarea id="stellen" name="stellen" required>'.$stellen.'</textarea>

                    <button type="submit" value="">Stellenanzeigen Aktualisieren</button>

                </form>';
        ?>
        </div>
    </body>
</html>

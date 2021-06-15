<?php
    $servername = "rdbms.strato.de";
    $username = "U3162331";
    $password = "t9BSpUrsdKGT4LhV";

	$sql = "SELECT stellen FROM stellenBaumgartner";

    $pdo = new PDO('mysql:host=rdbms.strato.de;dbname=DB3162331;charset=utf8', $username, $password);

    foreach ($pdo->query($sql) as $row) {
        $stellen = preg_replace("/((\r?\n)|(\r\n?))/", '}', $row['stellen']);
		$stellen = explode('}', $stellen);

		foreach ($stellen as $stelle) {
			if (strlen($stelle) > 3) {
				echo"<div class='anzeige'>
				<h2>$stelle</h2>
				<a class='button-light' href='/kontakt'>Jetzt Kontakt aufnehmen!</a>
				</div>";
			}

		}
    };

?>

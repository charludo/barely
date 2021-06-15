<?php
    $servername = "rdbms.strato.de";
    $username = "U3162331";
    $password = "t9BSpUrsdKGT4LhV";

    if( $_GET["sortby"]){
        if ($_GET["sortby"] == "titel"){
            $sql = "SELECT id, titel, beschreibung, bauherr, auftraggeber, architekt, baujahr, leistungsphasen, bilderpfad, archiviert FROM referenzenBaumgartner WHERE archiviert IS NULL OR archiviert='' ORDER BY titel";
        } elseif ($_GET["sortby"] == "projektbeginn"){
            $sql = "SELECT id, titel, beschreibung, bauherr, auftraggeber, architekt, baujahr, leistungsphasen, bilderpfad, archiviert FROM referenzenBaumgartner WHERE archiviert IS NULL OR archiviert='' ORDER BY projektbeginn DESC";
        }
    } elseif ( $_GET["type"]){
        if ($_GET["type"] == "verwaltung"){
            $sql = "SELECT id, titel, beschreibung, bauherr, auftraggeber, architekt, baujahr, leistungsphasen, bilderpfad, archiviert FROM referenzenBaumgartner WHERE gVerwaltung<>''  AND (archiviert IS NULL OR archiviert='') ORDER BY id DESC";
        } elseif ($_GET["type"] == "schule"){
            $sql = "SELECT id, titel, beschreibung, bauherr, auftraggeber, architekt, baujahr, leistungsphasen, bilderpfad, archiviert FROM referenzenBaumgartner WHERE gSchule<>''  AND (archiviert IS NULL OR archiviert='') ORDER BY id DESC";
        } elseif ($_GET["type"] == "labor"){
            $sql = "SELECT id, titel, beschreibung, bauherr, auftraggeber, architekt, baujahr, leistungsphasen, bilderpfad, archiviert FROM referenzenBaumgartner WHERE gLabor<>''  AND (archiviert IS NULL OR archiviert='') ORDER BY id DESC";
        } elseif ($_GET["type"] == "industrie"){
            $sql = "SELECT id, titel, beschreibung, bauherr, auftraggeber, architekt, baujahr, leistungsphasen, bilderpfad, archiviert FROM referenzenBaumgartner WHERE gIndustrie<>''  AND (archiviert IS NULL OR archiviert='') ORDER BY id DESC";
        } elseif ($_GET["type"] == "wohnen"){
            $sql = "SELECT id, titel, beschreibung, bauherr, auftraggeber, architekt, baujahr, leistungsphasen, bilderpfad, archiviert FROM referenzenBaumgartner WHERE gWohn<>''  AND (archiviert IS NULL OR archiviert='') ORDER BY id DESC";
        }  elseif ($_GET["type"] == "einzelhandel"){
            $sql = "SELECT id, titel, beschreibung, bauherr, auftraggeber, architekt, baujahr, leistungsphasen, bilderpfad, archiviert FROM referenzenBaumgartner WHERE gEinzelhandel<>''  AND (archiviert IS NULL OR archiviert='') ORDER BY id DESC";
        }  elseif ($_GET["type"] == "gastronomie"){
            $sql = "SELECT id, titel, beschreibung, bauherr, auftraggeber, architekt, baujahr, leistungsphasen, bilderpfad, archiviert FROM referenzenBaumgartner WHERE gGastronomie<>''  AND (archiviert IS NULL OR archiviert='') ORDER BY id DESC";
        }  elseif ($_GET["type"] == "arzt"){
            $sql = "SELECT id, titel, beschreibung, bauherr, auftraggeber, architekt, baujahr, leistungsphasen, bilderpfad, archiviert FROM referenzenBaumgartner WHERE gArzt<>''  AND (archiviert IS NULL OR archiviert='') ORDER BY id DESC";
        }  elseif ($_GET["type"] == "autohaus"){
            $sql = "SELECT id, titel, beschreibung, bauherr, auftraggeber, architekt, baujahr, leistungsphasen, bilderpfad, archiviert FROM referenzenBaumgartner WHERE gAutohaus<>''  AND (archiviert IS NULL OR archiviert='') ORDER BY id DESC";
        }

    } else {
        $sql = "SELECT id, titel, beschreibung, bauherr, auftraggeber, architekt, baujahr, leistungsphasen, bilderpfad, archiviert FROM referenzenBaumgartner WHERE archiviert IS NULL OR archiviert='' ORDER BY id DESC";
    }

    $pdo = new PDO('mysql:host=rdbms.strato.de;dbname=DB3162331;charset=utf8', $username, $password);

    foreach ($pdo->query($sql) as $row) {
        $id = $row['id'];
        $titel = $row['titel'];
        $beschreibung = $row['beschreibung'];
        $bauherr = $row['bauherr'];
        $auftraggeber = $row['auftraggeber'];
        $architekt = $row['architekt'];
        $baujahr = $row['baujahr'];
        $leistungsphasen = $row['leistungsphasen'];
        $bilderpfad = $row['bilderpfad'];

		echo "<div class='referenzWrapper'>
			<h2>$titel</h2>
			<div class='referenz'>
				<table class='referenzDaten'>";
					if (!empty($bauherr)){echo "<tr><th>Bauherr:</th><td>$bauherr</td></tr>";};
					if (!empty($auftraggeber)){echo "<tr><th>Auftraggeber:</th><td>$auftraggeber</td></tr>";};
					if (!empty($architekt)){echo "<tr><th>Architekt:</th><td>$architekt</td></tr>";};
					if (!empty($baujahr)){echo "<tr><th>Jahr der Ausführung:</th><td>$baujahr</td></tr>";};
					if (!empty($leistungsphasen)){echo "<tr><th>Leistungsphasen:</th><td>$leistungsphasen</td></tr>";};
				echo "</table>";
				echo "<div class='referenzText'>$beschreibung</div>";
				if (!empty($bilderpfad)){
					echo "<div class='referenzBilder'>";
						$images = glob($bilderpfad."*.jpg");

						foreach($images as $image) {
							echo '<a href="'.$image.'" data-lightbox="referenz'.$id.'"><img class="referenzBild referenzBild'.$id.'" src="/res/unveil/placeholder.png" data-src="'.$image.'"/></a>';
						}
					echo "</div>";
				};
			echo "</div>
		</div>";
    };

?>

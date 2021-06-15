<?php
    $servername = "rdbms.strato.de";
    $username = "U3162331";
    $password = "t9BSpUrsdKGT4LhV";
    
    // Only process POST reqeusts.
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $id = (int)$_POST["id"];
        $titel = $_POST["titel"];
        $beschreibung = $_POST["beschreibung"];
        $bauherr = $_POST["bauherr"];
        $auftraggeber = $_POST["auftraggeber"];
        $architekt = $_POST["architekt"];
        $baujahr = $_POST["baujahr"];
        $leistungsphasen = $_POST["leistungsphasen"];
        //$projektbeginn = $_POST["projektbeginn"];
        $archiviert = $_POST["archiviert"];
        $gVerwaltung = $_POST["gverwaltung"];
        $gSchule = $_POST["gschule"];
        $gLabor = $_POST["glabor"];
        $gIndustrie = $_POST["gindustrie"];
        $gWohn = $_POST["gwohn"];
		$gEinzelhandel = $_POST["geinzelhandel"];
		$gGastronomie = $_POST["ggastronomie"];
		$gArzt = $_POST["garzt"];
		$gAutohaus = $_POST["gautohaus"];
        /*echo $gWohn;*/
       
        $pdo = new PDO('mysql:host=rdbms.strato.de;dbname=DB3162331;charset=utf8', $username, $password);
        //$sql = "UPDATE referenzenBaumgartner SET titel='$titel', beschreibung='$beschreibung', bauherr='$bauherr', auftraggeber='$auftraggeber', architekt='$architekt', baujahr='$baujahr', leistungsphasen='$leistungsphasen', projektbeginn=2016-05-06, archiviert='$archiviert', gVerwaltung='$gVerwaltung', gSchule='$gSchule', gLabor='$gIndustrie', gWohn='$gWohn' WHERE id=$id";
        $sql = "UPDATE referenzenBaumgartner SET titel='$titel', beschreibung='$beschreibung', bauherr='$bauherr', auftraggeber='$auftraggeber', architekt='$architekt', baujahr='$baujahr', leistungsphasen='$leistungsphasen', archiviert='$archiviert', gVerwaltung='$gVerwaltung', gSchule='$gSchule', gLabor='$gIndustrie', gWohn='$gWohn', gEinzelhandel='$gEinzelhandel', gGastronomie='$gGastronomie', gArzt='$gArzt', gAutohaus='$gAutohaus' WHERE id=$id";
		$pdo->exec($sql);

        echo "Die Referenz wurde wurde auf folgende Daten aktualisiert:
        <h2>$titel</h2>
        <p>$beschreibung</p>
        <p>Bauherr: $bauherr</p>
        <p>Auftraggeber: $auftraggeber</p>
        <p>Architekt: $architekt</p>
        <p>Baujahr: $baujahr</p>
        <p>Leistungsphasen: $leistungsphasen</p>
        <p>&nbsp;</p>
        <p>&nbsp;</p>
        <a href='index.php'>Zurück zur Verwaltung der Referenzen</a>";
    };
?>
<?php
    $servername = "rdbms.strato.de";
    $username = "U3162331";
    $password = "t9BSpUrsdKGT4LhV";
    
    // Only process POST reqeusts.
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        // Get the form fields and remove whitespace.
        $titel = $_POST["titel"];
        $beschreibung = $_POST["beschreibung"];
        $bauherr = $_POST["bauherr"];
        $auftraggeber = $_POST["auftraggeber"];
        $architekt = $_POST["architekt"];
        $baujahr = $_POST["baujahr"];
        $leistungsphasen = $_POST["leistungsphasen"];
        $projektbeginn = $_POST["projektbeginn"];
        $gVerwaltung = $_POST["gverwaltung"];
        $gSchule = $_POST["gschule"];
        $gLabor = $_POST["glabor"];
        $gIndustrie = $_POST["gindustrie"];
        $gWohn = $_POST["gwohn"];
		$gEinzelhandel = $_POST["geinzelhandel"];
		$gGastronomie = $_POST["ggastronomie"];
		$gArzt = $_POST["garzt"];
		$gAutohaus = $_POST["gautohaus"];
        
        $valid_formats = array("jpg", "png", "gif");
        $identifierpre = preg_replace('~[\\\\/:*?"<>|,.äüöß ]~', '', $titel);
        $identifier=str_replace(array('ä','ö','ü','ß','Ä','Ö','Ü'),array('ae','oe','ue','ss','Ae','Oe','Ue'),$identifierpre); 
        //$path = "/home/strato/www/ib/www.ib-baumgartner.de/htdocs/baumgartner/images/".$identifier."/";
		$path = "/home/strato/www/ib/www.ib-baumgartner.de/htdocs//baumgartner/images/".$identifier."/";
		//$path = "/mnt/web024/c0/37/52552537/htdocs/baumgartner/images/".$identifier."/";
        mkdir($path);
		echo realpath(dirname(__FILE__));
        $displayPath = "../images/".$identifier."/";
        $count = 0;
        
        foreach ($_FILES['files']['name'] as $f => $name) {     
    	    if ($_FILES['files']['error'][$f] == 4) {
    	        continue; // Skip file if any error found
    	    }	       
    	    if ($_FILES['files']['error'][$f] == 0) {	           
    			if( ! in_array(pathinfo($name, PATHINFO_EXTENSION), $valid_formats) ){
    				$message[] = "$name is not a valid format";
    				continue; // Skip invalid file formats
    			}
    	        else{ // No error found! Move uploaded files 
    	            
    	            if(move_uploaded_file($_FILES["files"]["tmp_name"][$f], $path.$name))
    	            $count++; // Number of successfully uploaded file
					echo $path.$name;
    	        }
    	    }
    	}

       
        $pdo = new PDO('mysql:host=rdbms.strato.de;dbname=DB3162331;charset=utf8', $username, $password);
        $sql = "INSERT INTO referenzenBaumgartner (titel, beschreibung, bauherr, auftraggeber, architekt, baujahr, leistungsphasen, projektbeginn, bilderpfad, gVerwaltung, gSchule, gLabor, gIndustrie, gWohn, gEinzelhandel, gGastronomie, gArzt, gAutohaus) VALUES ('$titel', '$beschreibung', '$bauherr', '$auftraggeber', '$architekt', '$baujahr', '$leistungsphasen', '$projektbeginn', '$displayPath', '$gVerwaltung', '$gSchule', '$gLabor', '$gIndustrie', '$gWohn', '$gEinzelhandel', '$gGastronomie', '$gArzt', '$gAutohaus')";
        $pdo->exec($sql);

        echo "Folgende neue Referenz wurde angelegt:
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
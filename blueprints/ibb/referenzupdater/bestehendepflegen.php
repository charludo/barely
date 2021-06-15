<html>
    
    <head>
		<meta charset="utf8">
        <title>Bestehende Referenzen Pflegen</title>
        <link rel="stylesheet" type="text/css" href="styleupdater.css"/>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    </head>
    
    <body>
        <div class="contentContainer">
            <?php
                $servername = "rdbms.strato.de";
                $username = "U3162331";
                $password = "t9BSpUrsdKGT4LhV";
                
                $pdo = new PDO('mysql:host=rdbms.strato.de;dbname=DB3162331;charset=utf8', $username, $password);
                $sql = "SELECT id, titel, beschreibung, bauherr, auftraggeber, architekt, baujahr, leistungsphasen, projektbeginn, gVerwaltung, gSchule, gLabor, gIndustrie, gWohn, gEinzelhandel, gGastronomie, gArzt, gAutohaus FROM referenzenBaumgartner";
                foreach ($pdo->query($sql) as $row) {
                    $id = $row['id'];
                    $titel = $row['titel'];
                    $beschreibung = $row['beschreibung'];
                    $bauherr = $row['bauherr'];
                    $auftraggeber = $row['auftraggeber'];
                    $architekt = $row['architekt'];
                    $baujahr = $row['baujahr'];
                    $leistungsphasen = $row['leistungsphasen'];
                    //$projektbeginn = $row['projektbeginn'];
                    if (!empty($row['gVerwaltung'])){$gVerwaltung = 'checked';}else{$gVerwaltung='';};
                    if (!empty($row['gSchule'])){$gSchule = 'checked';}else{$gSchule='';};
                    if (!empty($row['gLabor'])){$gLabor = 'checked';}else{$gLabor='';};
                    if (!empty($row['gIndustrie'])){$gIndustrie = 'checked';}else{$gIndustrie='';};
                    if (!empty($row['gWohn'])){$gWohn = 'checked';}else{$gWohn='';};
					if (!empty($row['gEinzelhandel'])){$gEinzelhandel = 'checked';}else{$gEinzelhandel='';};
					if (!empty($row['gGastronomie'])){$gGastronomie = 'checked';}else{$gGastronomie='';};
					if (!empty($row['gArzt'])){$gArzt = 'checked';}else{$gArzt='';};
					if (!empty($row['gAutohaus'])){$gAutohaus = 'checked';}else{$gAutohaus='';};
                    
                    
                    echo '<h2 onclick="switchOpenReference(`#form'.$id.'`)">'.$titel.'</h2>
                    
                    <form class="referenceForm" id="form'.$id.'" method="post" action="updatereference.php">
        
                        <input type="text" id="titel" name="titel" maxlength="200" value="'.$titel.'" required>
                        
                        <textarea id="beschreibung" name="beschreibung" required>'.$beschreibung.'</textarea>
                        
                        <input type="text" id="bauherr" name="bauherr" maxlength="200" value="'.$bauherr.'">
                        
                        <input type="text" id="auftraggeber" name="auftraggeber" maxlength="200" value="'.$auftraggeber.'">
                        
                        <input type="text" id="architekt" name="architekt" maxlength="200" value="'.$architekt.'">
                        
                        <input type="text" id="baujahr" name="baujahr" maxlength="200" value="'.$baujahr.'">
                        
                        <input type="text" id="leistungsphasen" name="leistungsphasen" maxlength="200" value="'.$leistungsphasen.'">
                        
                        <!--<input type="date" id="projektbeginn" name="projektbeginn" maxlength="200" value="'.$projektbeginn.'" required pattern="[0-9]{4}-[0-9]{2}-[0-9]{2}">-->
                        <br><br>
                        <p>Gebäudetyp(en):
                        <label><input type="checkbox" name="gverwaltung" value="verwaltung" '.$gVerwaltung.'>Büro-/Verwaltungsgebäude</label>
                        <label><input type="checkbox" name="geschule" value="schule" '.$gSchule.'>Schule</label>
                        <label><input type="checkbox" name="glabor" value="labor" '.$gLabor.'>Laborgebäude</label>
                        <label><input type="checkbox" name="gindustrie" value="industrie '.$gIndustrie.'">Industriegebäude</label>
                        <label><input type="checkbox" name="gwohn" value="wohn" '.$gWohn.'>Wohngebäude</label>
						<label><input type="checkbox" name="geinzelhandel" value="einzelhandel" '.$gEinzelhandel.'>Einzelhandel</label>
						<label><input type="checkbox" name="ggastronomie" value="gastronomie" '.$gGastronomie.'>Gastronomie</label>
						<label><input type="checkbox" name="garzt" value="arzt" '.$gArzt.'>Arztpraxen</label>
						<label><input type="checkbox" name="gautohaus" value="autohaus" '.$gAutohaus.'>Autohäuser</label></p>

                        <br><br>
                        
                        <label><input type="checkbox" name="archiviert" value="archiviert">Referenz Archivieren</label>
                        
                        <input type="hidden" name="id" value='.$id.'/> 
                        
                        <button type="submit" value="">Referenz Aktualisieren</button>
                        
                    </form>
                    <hr />';
                    
                };
                    
            ?>
            
            
        </div>
        
        <script>
            function switchOpenReference(whichReference){
                $(whichReference).slideToggle( "fast", function() {
                    
                });
            };
        </script>
    </body>
    
</html>
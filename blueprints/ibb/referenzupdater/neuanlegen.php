<html>
    
    <head>
		<meta charset="utf8">
        <title>Neue Referenz anlegen</title>
        <link rel="stylesheet" type="text/css" href="styleupdater.css"/>
    </head>
    
    <body>
        <div class="contentContainer">
            <form id="newReferenceForm" method="post" action="newreference.php" enctype="multipart/form-data">
                <h2>Neue Referenz Anlegen:</h2>

                <input type="text" id="titel" name="titel" maxlength="200" placeholder="Referenztitel*" required>
                
                <textarea id="beschreibung" name="beschreibung" placeholder="Beschreibungstext*" required></textarea>
                
                <input type="text" id="bauherr" name="bauherr" maxlength="200" placeholder="Bauherr">
                
                <input type="text" id="auftraggeber" name="auftraggeber" maxlength="200" placeholder="Auftraggeber">
                
                <input type="text" id="architekt" name="architekt" maxlength="200" placeholder="Architekt">
                
                <input type="text" id="baujahr" name="baujahr" maxlength="200" placeholder="Jahr der Ausführung">
                
                <input type="text" id="leistungsphasen" name="leistungsphasen" maxlength="200" placeholder="Leistungsphasen">
                
                <input type="date" id="projektbeginn" name="projektbeginn" maxlength="200" placeholder="Projektbeginn* yyyy-mm-dd" required pattern="[0-9]{4}-[0-9]{2}-[0-9]{2}">
                <br><br>
                <p>Gebäudetyp(en):
                <label><input type="checkbox" name="gverwaltung" value="verwaltung">Büro-/Verwaltungsgebäude</label>
                <label><input type="checkbox" name="gschule" value="schule">Schule</label>
                <label><input type="checkbox" name="glabor" value="labor">Laborgebäude</label>
                <label><input type="checkbox" name="gindustrie" value="industrie">Industriegebäude</label>
                <label><input type="checkbox" name="gwohn" value="wohn">Wohngebäude</label>
				<label><input type="checkbox" name="geinzelhandel" value="einzelhandel">Einzelhandel</label>
				<label><input type="checkbox" name="ggastronomie" value="gastronomie">Gastronomie</label>
				<label><input type="checkbox" name="garzt" value="arzt">Arztpraxen</label>
				<label><input type="checkbox" name="gautohaus" value="autohaus">Autohäuser</label></p>
                <br><br>
                <p>Projektbilder hochladen:
                <input type="file" id="file" name="files[]" multiple="multiple" accept="image/*"/></p>
                
                <button type="submit" value="">Referenz Einfügen</button>
                
            </form>
        </div>
    </body>
    
</html>
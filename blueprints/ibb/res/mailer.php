<?php
    // Only process POST reqeusts.
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        // Get the form fields and remove whitespace.
        $name_required = strip_tags(trim($_POST["name_required"]));
        $name = isset($_POST["name"]) ? strip_tags(trim($_POST["name"])) : "Ohne Name";
		$name = str_replace(array("\r","\n"),array(" "," "),$name);
        $email = filter_var(trim($_POST["email"]), FILTER_SANITIZE_EMAIL);
        $tel = isset($_POST["phone"]) ? $tel = trim($_POST["phone"]) : "";
        $nachricht = trim($_POST["message"]);

        // Check that data was sent to the mailer.
        if ( empty($nachricht) OR !filter_var($email, FILTER_VALIDATE_EMAIL) OR (!empty($name_required))) {
            // Set a 400 (bad request) response code and exit.
            http_response_code(400);
            echo "Ups! Etwas ist schief gelaufen und Ihre Nachricht konnte nicht gesendet werden.";
            exit;
        }

        // Set the recipient email address.
        $recipient = "mail@ib-baumgartner.de";

        // Set the email subject.
        $subject = "Nachricht auf Ihrer Website";

        // Build the email content.
        $email_content .= "Name: $name\n";
        $email_content .= "Email: $email\n";
        $email_content .= "Tel: $tel\n\n";
        $email_content .= "Nachricht:\n$nachricht\n";

        // Build the email headers.
        $header = "From: $name <$email>\r\n";
        $header .= "Content-Type:  text/plain; Charset=utf-8\r\n";

        // Send the email.
        if (mail($recipient, $subject, $email_content, $header)) {
            // Set a 200 (okay) response code.
            http_response_code(200);
            echo "Vielen Dank! Ihre Nachricht wurde erfolgreich gesendet, und wir werden in Kürze auf Sie zurückkommen!";
        } else {
            // Set a 500 (internal server error) response code.
            http_response_code(500);
            echo "Ups! Etwas ist schief gelaufen und Ihre Nachricht konnte nicht gesendet werden.";
        }

    } else {
        // Not a POST request, set a 403 (forbidden) response code.
        http_response_code(403);
        echo "Ups! Etwas ist schief gelaufen und Ihre Nachricht konnte nicht gesendet werden.";
    }

?>

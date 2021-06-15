$(function() {

	// Get the form.
	var form = $('#kontaktForm');

	// Get the messages div.
	var formMessages = $('#erfolgsNachricht');

	// Set up an event listener for the contact form.
	$(form).submit(function(e) {
		// Stop the browser from submitting the form.
		e.preventDefault();
		// Serialize the form data.
		var formData = $(form).serialize();

		// Submit the form using AJAX.
		$.ajax({
			type: 'POST',
			url: $(form).attr('action'),
			data: formData
		})
		.done(function(response) {
			// Make sure that the formMessages div has the 'success' class.
			$(formMessages).removeClass('error');
			$(formMessages).addClass('success');

			// Set the message text.
			$(formMessages).text(response);

			// Clear the form.
			//$('#name').val('');
			//$('#email').val('');
			//$('#tel').val('');
			//$('#nachricht').val('');
			$("#kontaktForm").trigger('reset');
		})
		.fail(function(data) {
			// Make sure that the formMessages div has the 'error' class.
			$(formMessages).removeClass('success');
			$(formMessages).addClass('error');

			// Set the message text.
			if (data.responseText !== '') {
				$(formMessages).text(data.responseText);
			} else {
				$(formMessages).text('Ups! Etwas ist schief gelaufen und Ihre Nachricht Konte nicht gesendet werden..');
			}
		});

	});






	// Get the form.
	var form2 = $('#footerForm');

	// Get the messages div.
	var formMessages2 = $('#footerErfolgsNachricht');

	// Set up an event listener for the contact form.
	$(form2).submit(function(e) {
		// Stop the browser from submitting the form.
		e.preventDefault();
		// Serialize the form data.
		var formData2 = $(form2).serialize();

		// Submit the form using AJAX.
		$.ajax({
			type: 'POST',
			url: $(form2).attr('action'),
			data: formData2
		})
		.done(function(response) {
			// Make sure that the formMessages div has the 'success' class.
			$(formMessages2).removeClass('error');
			$(formMessages2).addClass('success');

			// Set the message text.
			$(formMessages2).text(response);

			// Clear the form.
			//$('#name').val('');
			//$('#email').val('');
			//$('#tel').val('');
			//$('#nachricht').val('');
			$("#footerForm").trigger('reset');
		})
		.fail(function(data) {
			// Make sure that the formMessages div has the 'error' class.
			$(formMessages2).removeClass('success');
			$(formMessages2).addClass('error');

			// Set the message text.
			if (data.responseText !== '') {
				$(formMessages2).text(data.responseText);
			} else {
				$(formMessages2).text('Ups! Etwas ist schief gelaufen und Ihre Nachricht Konte nicht gesendet werden..');
			}
		});

	});

});

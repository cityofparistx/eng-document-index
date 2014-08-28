$('tbody tr').click( function() {
		//window.location = $(this).attr('href');
        url = $(this).attr('href');
        window.open(url, "_blank");
	});

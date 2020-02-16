(function () {
	var rec = new GlideRecord('u_new_hire');
	var user = gs.getUserID();
	var currentUser = gs.getUser();

	rec.addQuery('u_user', user);
	rec.query();

	if (rec.next()) {
		//data.firstName = currentUser.getFirstName();
		//data.lastName = currentUser.getLastName();
		data.firstName = rec.getValue('u_first_name');
		data.middleName = rec.getValue('u_middle_name');
		data.lastName = rec.getValue('u_last_name');
		data.gender = rec.getValue('u_gender');
		data.contact = rec.getValue('u_contact_number');
		data.passport = rec.getValue('u_passport_number');
		data.pan = rec.getValue('u_pan_number');
		data.aadhar = rec.getValue('u_aadhar_number');
		data.dob = rec.getValue('u_date_of_birth');
		data.nationality = rec.getValue('u_nationality');
		data.line_1 = rec.getValue('u_line_1');
		data.line_2 = rec.getValue('u_line_2');
		data.line_3 = rec.getValue('u_line_3');
		data.isConfirmed = rec.getValue('u_is_confirmed');
	}
	if (input && input.changes_made) {
		rec.setValue("u_first_name", input.changes_made[0]);
		rec.setValue("u_last_name", input.changes_made[1]);
		rec.setValue("u_gender", input.changes_made[2]);
		rec.setValue("u_email_address", input.changes_made[3]);
		rec.setValue("u_contact_number", input.changes_made[4]);
		rec.setValue("u_date_of_birth", input.changes_made[5]);
		rec.setValue("u_passport_number", input.changes_made[6]);
		rec.setValue("u_pan_number", input.changes_made[7]);
		rec.setValue("u_aadhar_number", input.changes_made[8]);
		rec.setValue("u_nationality", input.changes_made[9]);
		rec.setValue("u_line_1", input.changes_made[10]);
		rec.setValue("u_line_2", input.changes_made[11]);
		rec.setValue("u_line_3", input.changes_made[12]);
		rec.setValue("u_line1", input.changes_made[13]);
		rec.setValue("u_line2", input.changes_made[14]);
		rec.setValue("u_line3", input.changes_made[15]);
		rec.setValue("u_middle_name", input.changes_made[16]);
		rec.update();
	}

})();
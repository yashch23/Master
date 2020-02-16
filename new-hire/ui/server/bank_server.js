(function () {

    if (input) {
        var stringClassify = input.string_classify;

        var rec = new GlideRecord('u_new_hire');
        var user = gs.getUserID();

        rec.addQuery('u_user', user);
        rec.query();

        if (rec.next()) {
            rec.setValue('u_micr', stringClassify.micr);
            rec.setValue('u_bank_name', stringClassify.bank_name);
            rec.setValue('u_acc_no', stringClassify.account_number);
            rec.setValue('u_ifsc', stringClassify.ifsc);
        }
        else {
            rec.setValue('u_micr', stringClassify.micr);
            rec.setValue('u_bank_name', stringClassify.bank_name);
            rec.setValue('u_acc_no', stringClassify.account_number);
            rec.setValue('u_ifsc', stringClassify.ifsc);
        }
    }
})();

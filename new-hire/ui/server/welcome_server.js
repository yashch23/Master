(function () {
  /* populate the 'data' object */
  /* e.g., data.table = $sp.getValue('table'); */
  if (input) {
    var stringClassify = input.string_classify;
    var stringClassify1 = input.string_classify1;

    var entity = ["INCOME", "TAX", "DEPARTMENT", "INDIA.", "GOVT.", "Permanent", "Account", "Number",
      "DOB", "Male", "fA",
      "REPUBLIC", "Given", "Names", "Coiry", "Conte", "STEIN", "Place", "Passport", "No.", "<<",
      "REGISTRATION", "ADVISED", "REGISTER", "Spouse", "Mother", "Father", "Legal", "Guardian", "File", "Name"];

    var documents = [];

    //Entites for PAN 
    documents.push([1, 1, 1, 1, 1, 1, 1, 1,
      0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ]);

    //Entites for Aadhar Card 
    documents.push([0, 0, 0, 0, 0, 0, 0, 0,
      1, 1, 1,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0]);

    //Entites for Bank Cheque
    documents.push([0, 0, 0, 1, 0, 0, 0, 0,
      0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0]);

    //Entites for Passport Frontside
    documents.push([0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0,
      1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0]);

    //Entites for Passport Backside       
    documents.push([0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      1, 1, 1, 1, 1, 1, 1, 1, 1, 1]);

    var i;
    var imageEntities = [];

    for (i = 0; i < entity.length; i++) {
      var flag = 0;
      if (stringClassify.match(entity[i]) == entity[i]) {
        flag = 1;
        imageEntities.push(1);
      }
      if (flag == 0)
        imageEntities.push(0);
    }

    var p, q;
    var array = [];

    for (p = 0; p < documents.length; p++) {
      var dotProduct = 0;
      var magnitudeA = 0;
      var magnitudeB = 0;
      for (q = 0; q < documents[p].length; q++) {
        dotProduct += (imageEntities[q] * documents[p][q]);
        magnitudeA += (imageEntities[q] * imageEntities[q]);
        magnitudeB += (documents[p][q] * documents[p][q]);
      }
      magnitudeA = Math.sqrt(magnitudeA);
      magnitudeB = Math.sqrt(magnitudeB);
      var similarity = (dotProduct) / (magnitudeA * magnitudeB);
      array.push(similarity);
    }

    var array1 = ["PAN", "Aadhar Card", "Bank Cheque", "Passport Frontside", "Passport Backside"];

    var rec = new GlideRecord('u_new_hire');
    var user = gs.getUserID();
    rec.addQuery('u_user', user);
    rec.query();

    var qw;
    if (array1[array.indexOf(Math.max.apply(Math, array))] == "Passport Frontside") {
      var resultForPassport = stringClassify.replace(/\s\s+/g, ' ').trim().match(/[A-Z][0-9]{7}/g);

      var s = 0, q = 0;
      for (r = 0; r < stringClassify1.length; r++) {
        gs.info("stringClassify1 ==== " + stringClassify1[r]);
        if (stringClassify1[r].match("P<")) {
          s = r;
          if (!s.trim()) {
            var lastTwoLines = (stringClassify1.slice(r, stringClassify1.length).join("").replaceAll(" ", "").replaceAll("\.", ""));
            s = 0;
            qw = lastTwoLines.split("");
            break;
          }
        }
      }

      var lastname = [];
      var firstname = [];
      var nation = [];
      var nationality = " "

      if (qw) {
        for (q = 2; q < 5; q++) {
          nation.push(qw[q])
        }
        if (nation.join("") == "IND") {
          nationality = "Indian"
        }

        if (qw[q]) {
          for (; qw[q] != "<"; q++) {
            lastname.push(qw[q])
            if (!qw) {
              break;
            }
          }
        }

        for (e = q + 2; qw[e] != "<"; e++) {
          firstname.push(qw[e])
          if (!qw[e]) {
            break;
          }
        }
      }

      if (rec.next()) {
        rec.setValue('u_passport_number', resultForPassport ? resultForPassport[0] : '');
        rec.setValue('u_nationality', nationality);
        rec.setValue('u_first_name', firstname.join(""));
        rec.setValue('u_last_name', lastname.join(""));
      }
      else {
        rec.setValue('u_passport_number', resultForPassport ? resultForPassport[0] : '');
        rec.setValue('u_nationality', nationality);
        rec.setValue('u_first_name', firstname.join(""));
        rec.setValue('u_last_name', lastname.join(""));
        rec.setValue('u_user', user);
      }
    }

    else if (array1[array.indexOf(Math.max.apply(Math, array))] == "Passport Backside") {
      if (rec.next()) {
        //rec.setValue('line_1', address[0]);
        //rec.setValue('line_2', address[1]);
        //rec.setValue('line_3', address[2]);
      }
      else {
        //rec.setValue('line_1', address[0]);
        //rec.setValue('line_2', address[1]);
        //rec.setValue('line_3', address[2]);
        rec.setValue('u_user', user);
      }
    }

    else if (array1[array.indexOf(Math.max.apply(Math, array))] == "PAN") {
      var resultForPanCard = stringClassify.match(/[A-Z]{5}[0-9]{4}[A-Z]/i);
      var foundForPanCard = stringClassify.match(resultForPanCard);
      /* var dateOfBirth = stringClassify.match(/[0-9]{2}(\/)[0-9]{2}(\/)[0-9]{4}/gmi);
       var foundDateOfBirth = stringClassify.match(dateOfBirth);
       console.log(foundDateOfBirth[0]);*/

      if (rec.next()) {
        rec.setValue('u_pan_number', foundForPanCard[0]);
        //rec.setValue('u_date_of_birth', foundDateOfBirth[0]);
      }
      else {
        rec.setValue('u_pan_number', foundForPanCard[0]);
        //rec.setValue('u_date_of_birth', foundDateOfBirth[0]);
        rec.setValue('u_user', user);
      }
    }

    else if (array1[array.indexOf(Math.max.apply(Math, array))] == "Aadhar Card") {
      var a = 0, b = 0;
      for (r = 0; r < stringClassify1.length; r++) {
        if (stringClassify1[r].match("Address:")) {
          a = r;
          break;
        }
      }

      var line1 = " ";
      var line2 = " ";
      var line3 = " ";

      qw = stringClassify1[a + 1].split("")

      if (typeof qw !== "undefined") {
        for (c = 0; c < qw.length; c++) {
          if (qw[c] == ",") {
            b = c;
            break;
          }
        }
        if (b != 0) {
          for (c = b + 1; qw[c] != "/n" && c < qw.length; c++) {
            line1 = line1 + qw[c]
          }
        }
      }
      line1 = line1 + " "

      var f = 0;
      for (f = 0; f < stringClassify1[a + 2].length && stringClassify1[a + 2][f] != ","; f++) {
        line1 = line1 + stringClassify1[a + 2][f]
      }
      for (y = f; y < stringClassify1[a + 2].length; y++) {
        line2 = line2 + stringClassify1[a + 2][y]
      }
      line2 += " "
      f = 0;
      for (f = 0; f < stringClassify1[a + 3].length && +stringClassify1[a + 3][f] != ","; f++) {
        line2 = line2 + stringClassify1[a + 3][f]
      }
      for (y = f; f < stringClassify1[a + 3].length; f++) {
        line2 = line2 + stringClassify1[a + 3][f];
      }
      line3 += " "

      for (f = 0; f < stringClassify1[a + 4].length; f++) {
        line2 = line2 + stringClassify1[a + 4][f];
      }

      if (stringClassify1[a + 5]) {
        for (f = 0; f < stringClassify1[a + 5].length; f++) {
          line3 = line3 + stringClassify1[a + 5][f];
        }
      }


      var resultForAadharCard = stringClassify.match(/[0-9]{4}\s[0-9]{4}\s[0-9]{4}/i);
      var foundForAadharCard = stringClassify.match(resultForAadharCard);


      var gender = stringClassify.match(/male|emale|females/i);
      var foundGender = stringClassify.match(gender);

      if (foundGender != 'MALE') { foundGender = 'FEMALE' }
      var dateOfBirth = stringClassify.match(/[0-9]{2}(\/)[0-9]{2}(\/)[0-9]{4}/gmi);
      var foundDateOfBirth = stringClassify.match(dateOfBirth);

      var foundContact = '';
      for (x = 0; x < stringClassify1.length; x++) {
        if (!isNaN(stringClassify1[x]) && stringClassify1[x].length == 10) {
          foundContact = stringClassify1[x]
          break;
        }
      }

      var userRecordExists = rec.next();
      rec.setValue('u_aadhar_number', foundForAadharCard[0]);
      rec.setValue('u_gender', foundGender);
      rec.setValue('u_date_of_birth', foundDateOfBirth[0]);
      rec.setValue('u_line_1', line1.trim().replace(/[^a-zA-Z0-9 ]/g, ''));
      rec.setValue('u_line_2', line2.trim().replace(/[^a-zA-Z0-9 ]/g, ''));
      rec.setValue('u_line_3', line3.trim().replace(/[^a-zA-Z0-9 ]/g, ''));
      if (!userRecordExists) {
        rec.setValue('u_user', user);
      }
    }

    rec.update();
  }
})();
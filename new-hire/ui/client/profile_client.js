function($scope) {
	var c = this;

	$scope.confirmDetails = true;

	$scope.clicked = function () {
		var confirmed = c.data.isConfirmed;
		console.log(confirmed);
		if (confirmed == 1) {
			$scope.confirmDetails = false;
			$scope.confirmed = true;
		} else {
			alert('Please check confimation checkbox');
		}
	}

	$scope.copyAddress = function () {
		c.data.line1 = c.data.line_1;
		c.data.line2 = c.data.line_2;
		c.data.line3 = c.data.line_3;
	}

	var changesMade = [];

	$scope.saved = function () {
		changesMade.push(angular.element('#firstName')[0].value);
		changesMade.push(angular.element('#lastName')[0].value);
		changesMade.push(angular.element('#gender1')[0].value);
		changesMade.push(angular.element('#email')[0].value);
		changesMade.push(angular.element('#contactNumber')[0].value);
		changesMade.push(angular.element('#dob')[0].value);
		changesMade.push(angular.element('#passportNumber')[0].value);
		changesMade.push(angular.element('#panNumber')[0].value);
		changesMade.push(angular.element('#aadharNumber')[0].value);
		changesMade.push(angular.element('#nationality1')[0].value);
		changesMade.push(angular.element('#line_1')[0].value);
		changesMade.push(angular.element('#line_2')[0].value);
		changesMade.push(angular.element('#line_3')[0].value);
		changesMade.push(angular.element('#line1')[0].value);
		changesMade.push(angular.element('#line2')[0].value);
		changesMade.push(angular.element('#line3')[0].value);
		changesMade.push(angular.element('#middleName')[0].value);
		var newInputs = {
			changes_made: changesMade
		}
		c.server.get(newInputs);
	}

}
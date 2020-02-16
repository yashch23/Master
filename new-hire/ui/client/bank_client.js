function($scope, $http, $timeout, $rootScope) {
    var c = this;
    $scope.readFile = function () {
        $scope.uploaded = false;
        $scope.conti = false;

        function createBlob(dataURL) {
            var BASE64_MARKER = ";base64,";
            if (dataURL.indexOf(BASE64_MARKER) == -1) {
                var parts = dataURL.split(",");
                var contentType = parts[0].split(":")[1];
                var raw = decodeURIComponent(parts[1]);
                return new Blob([raw], { type: contentType });
            }
            var parts = dataURL.split(BASE64_MARKER);
            var contentType = parts[0].split(":")[1];
            var raw = window.atob(parts[1]);
            var rawLength = raw.length;
            var uInt8Array = new Uint8Array(rawLength);
            for (var i = 0; i < rawLength; ++i) {
                uInt8Array[i] = raw.charCodeAt(i);
            }
            return new Blob([uInt8Array], { type: contentType });
        }

        var files = document.getElementById("inputImage").files;
        var newInputs = [];
        function readAndPreview(file) {
            var reader = new FileReader();

            reader.addEventListener('load', function () {

                var image = new Image();
                image.height = 100;
                image.title = file.name;
                image.src = this.result;
                bank_cheque.appendChild(image);

                var dataURL = reader.result;
                var data = createBlob(dataURL);
                var config = {
                    method: "POST",
                    //url:"https://192.168.1.4:3310/document_details?doc_type=bank",
                    url: "https://10.160.70.41:3310/document_details?doc_type=bank",
                    headers: {
                        "Content-Type": "application/octet-stream",
                        "Accept": "application/json"
                    },
                    data: data
                };

                $rootScope.$broadcast('showSpinner', true);
                $http(config).then(function successCallback(response) {
                    $timeout(function () {
                        var ocr = response.data;
                        document.getElementById("account_number").value = ocr.account_number;
                        document.getElementById("bank_name").value = ocr.bank_name;
                        document.getElementById("micr_code").value = ocr.micr;
                        document.getElementById("ifsc_code").value = ocr.ifsc;


                        newInputs.push({
                            string_classify: ocr
                            //string_classify1 : ocr1
                        })

                        $rootScope.$broadcast('showSpinner', false);
                        $scope.uploaded = true;

                    }, 5000)

                }, function errorCallback(response) {
                    $scope.error = response.statusText;
                    spUtil.addErrorMessage('Things did not go well')
                    $rootScope.$broadcast('showSpinner', false);
                });
            }, false);
            reader.readAsDataURL(file);
        }

        if (files) {
            [].forEach.call(files, readAndPreview);
        }

        c.updateImage = function () {
            $rootScope.$broadcast('showSpinner', true);
            for (i = 0; i < newInputs.length; i++) {
                c.server.get(newInputs[i]);
                c.useUpdate = function () {
                    c.server.update();
                }
            }

            $rootScope.$broadcast('showSpinner', false);
            $scope.uploaded = false;
            $scope.conti = true;
        }
    }
}
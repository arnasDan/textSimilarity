'use strict';

(function () {
    Office.initialize = function (reason) {
        $(document).ready(function () {
            if (Office.context.requirements.isSetSupported('WordApi', 1.1)) {
                $('#processSelection').click(processSelection);
                $('#supportedVersion').html('This code is using Word 2016 or later.');
            }
            else {
                $('#supportedVersion').html('This code requires Word 2016 or later.');
            }
        });
    };

    function processSelection() {
        var text;
        Word.run(function (context) {
            var range = context.document.getSelection();
            range.load('text');
            context.sync()
                .then(function () {
                    //$('#content-main').append(range.text);
                    text = range.text;
                    console.log(range.text + " test");
                    $.ajax({
                        url: "process_text",
                        data: {
                            text: range.text
                        },
                        type: "GET",
                        dataType: "html",
                        success: function(results) {
                            $('#content-main').append(results);
                        },
                        error: function(xhr, status) {
                            console.log(status);
                        }
                        
                        
                    });
                });
        });
    };
})();
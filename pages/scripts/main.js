'use strict';

(function () {
    Office.initialize = function (reason) {
        $(document).ready(function () {
            if (Office.context.requirements.isSetSupported('WordApi', 1.1)) {
                $('#searchSelection').click(searchSelection);
                $('#searchAll').click(searchAll);
                $('#supportedVersion').html('This code is using Word 2016 or later.');
            }
            else {
                $('#supportedVersion').html('This code requires Word 2016 or later.');
            }
        });
    };

    function searchText(text) {
        $.ajax({
            url: "process_text",
            data: {
                text: text
            },
            type: "GET",
            dataType: "html",
            success: function(results) {
                $('#results').html(results);
            },
            error: function(xhr, status) {
                console.log(status);
            }
        });
    }

    function searchAll() {
        Word.run(function (context) {
            var documentBody = context.document.body;
            context.load(documentBody);
            context.sync()
                .then(function () {
                    searchText(documentBody.text);
                });
        });
    }

    function searchSelection() {
        Word.run(function (context) {
            var range = context.document.getSelection();
            range.load('text');
            context.sync()
                .then(function () {
                    searchText(range.text);
                });
        });
    };
})();
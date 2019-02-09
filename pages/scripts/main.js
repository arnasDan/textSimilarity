'use strict';

(function () {
    Office.initialize = function (reason) {
        $(document).ready(function () {
            if (Office.context.requirements.isSetSupported('WordApi', 1.1)) {
                $('#searchSelection').click(searchSelection);
                $('#searchAll').click(searchAll);
            }
            else {
                $('body').html('Word 2016 or later is required to use this add-in.');
            }
        });
    };

    function searchText(text) {
        $('#results').fadeOut('normal', function () {
            $('#results-spinner').show();
            $.ajax({
                url: "process-text",
                data: {
                    text: text
                },
                type: "GET",
                dataType: "html",
                success: function(results) {
                    $('#results-spinner').hide();
                    $('#results').html(results);
                    $('#results').fadeIn();
                },
                error: function(xhr, status) {
                    console.log(status);
                }
            });
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
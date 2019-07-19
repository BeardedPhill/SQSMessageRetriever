function prettifyJson() {
    $.each($('.json-metadata'), function(index, domElem) {
        if($(domElem).attr('data-format') === 'html')
            return;

        // Handle double encoding
        var elemText = $(domElem).text().trim();
        if(elemText.includes('\\"')){
            elemText = $.parseJSON(elemText)
        }

        renderjson.set_show_to_level(1);
        // Reveal hidden 'json-metadata' elements (if necessary),
        // to avoid popping of newly formatted JSON
        $(domElem).html(
          renderjson($.parseJSON(elemText))
        ).slideDown("fast");


        $(domElem).attr('data-format', 'html');
    });
}

$(document).ready(function(){
  prettifyJson();
});

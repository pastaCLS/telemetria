$(document).ready(function() {
    for(i = 1; document.getElementById("pestana"+i.toString()); i++) {

        $("#pestana"+i.toString()).click(function() {
            item = $(this).attr('id');
            num = parseInt(item.substring(item.length-1));

            /* este codigo no soporta mas de 10 pestanas */
            for( i = 1; document.getElementById("pestana"+i.toString()); i++) {
                if (i == num) {
                    $("#pestana" + i.toString()).addClass("activa");
                    $("#contenedor" + i.toString()).css("zIndex", 10);
                    $("#contenedor" + i.toString()).show();
                } else {
                    $("#pestana" + i.toString()).removeClass("activa");
                    $("#contenedor" + i.toString()).css("zIndex", 9);
                    $("#contenedor" + i.toString()).hide();
                }
            }
        });
    }

});

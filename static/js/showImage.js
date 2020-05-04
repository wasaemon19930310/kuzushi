$(function() {
    var file = $('input[type=file]').prop('files')[0];
    if(file == null) {
        $(".btn").prop("disabled", true);
    }
    $('input[type=file]').change(function() {
        var file = $(this).prop('files')[0];
        $(".btn").prop("disabled", false);
        $('#result img').remove();
        var fileReader = new FileReader();
        fileReader.onloadend = function() {
            $(".img_prev").html('<img src="' + fileReader.result + '"/>');
        }
        fileReader.readAsDataURL(file);
    });
});
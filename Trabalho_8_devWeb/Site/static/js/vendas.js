$(document).ready(function() {
$(".btn-comprar").click(function () {
    let form = $(this).parent();
    let row = $(this).parent().parent().parent();
    let td = row.find('td:eq(3)');

    var input = "<input type='hidden' name='produto_qtd' value='" + td.find('input')[0].value + "' >"
    form.append(input)


    let url = $(form).attr('action');
    let formData = $(form).serializeArray();
    $.ajax({
      type: "POST",
      url: url,

      data: formData,

      success: function(result) {
        alert(result.name);
      },
      error: function(result) {
        alert('error');
      }
    });
 });

$(".btn-removerProd").click(function () {
    let form = $(this).parent();
    let row = $(this).parent().parent().parent();
    let td = row.find('td:eq(4)');

    var input = "<input type='hidden' name='produto_qtd' value='" + td.find('input')[0].value + "' >"
    form.append(input)

    let url = $(form).attr('action');
    let formData = $(form).serializeArray();
    $.ajax({
      type: "POST",
      url: url,

      data: formData,

      success: function(result) {
          location.reload(true);
      },
      error: function(result) {
        alert('error');
      }
    });
 });

});
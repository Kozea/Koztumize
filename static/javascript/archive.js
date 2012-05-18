function submitSearch(filename){
  alert(filename);
  $.ajax({
    type: 'POST',
    url: 'http://kozea.local:5000/archive_get',
    data: 'filename='+filename,
    success: function (res) {
                $("#archive").html(res);
                alert('succes');
              }
  }); 
}



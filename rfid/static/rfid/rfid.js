$(document).ready(function() {
    $('.rfid-btn').on('click', function(event){
      event.preventDefault()
      var $this = $(this);
      $.ajax({
          url: $this.attr('href'),
          success: function(data){
            alert("success")
          },
          error: function(data){
            alert("error");
          }
      });
    });
  }
);

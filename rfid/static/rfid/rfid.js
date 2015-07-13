$(document).ready(function() {
    $('.rfid-btn').on('click', function(event){
      event.preventDefault()
      var $this = $(this);
      $('.fa', $this).attr('class','fa fa-cog fa-spin');
      $.ajax({
          url: $this.attr('href'),
          success: function(data) {
            $('.fa', $this).attr('class','fa fa-unlock')
            window.setTimeout(function(element){
              element.attr('class', 'fa fa-lock');
            }, 5000, $('.fa', $this));
          },
          error: function(data) {
            $('.fa', $this).attr('class','fa fa-lock')
            $('#alerts').append(
              '<div class="alert alert-danger alert-dismissable">'+
              '<button class="close" aria-hidden="true" data-dismiss="alert" type="button">×</button>'+
                'Unable to unlock the ' + $this.text().toLowerCase() + '.' +
              '</div>');
          }
      });
    });
  }
);

$("#theform").submit(function(event) 
{
  event.preventDefault();
  $("#alertdiv").removeClass();
  $("#alertdiv").empty();
  
  $("#submit_btn").empty();
  $("#submit_btn").append('<i class="fa fa-refresh fa-spin"></i> Loggin in');
  $("#submit_btn").attr("disabled", true);

  $.ajax(
  {
      url: '/login',
      data: $('#theform').serialize(),
      type: 'POST',
      success: function(response) 
      {
        console.log(JSON.stringify(response));
        if(response[0].auth == "true")
        {
          window.location = "landing.html";
        }
        else
        {
          show_incorrect();
        }
      },
      error: function(error) 
      {
        console.log($('#theform').serialize());
        console.log(error);
        show_error();
      }
    });
});

function show_incorrect()
{
  $("#alertdiv").css("display", "block");
  $("#alertdiv").addClass("alert alert-danger");
  $("#alertdiv").append('<a href="#" id="close_me" class="close" data-dismiss="alert" aria-label="close">&times;</a>');
  $("#alertdiv").append("<strong>Incorrect!</strong> Wrong username or password.");

  $("#submit_btn").empty();
  $("#submit_btn").append('Submit');
  $("#submit_btn").attr("disabled", false);
}

function show_error()
{
  $("#alertdiv").css("display", "block");
  $("#alertdiv").addClass("alert alert-danger");
  $("#alertdiv").append('<a href="#" id="close_me" class="close" data-dismiss="alert" aria-label="close">&times;</a>');
  $("#alertdiv").append("Something went wrong. Please try again.");

  $("#submit_btn").empty();
  $("#submit_btn").append('Submit');
  $("#submit_btn").attr("disabled", false);
}

$(document).on("click", "#close_me", function(event)
{
  event.preventDefault();
  $("#alertdiv").fadeOut("slow", function()
  {
    $("#alertdiv").removeClass();
    $("#alertdiv").empty();
  })
});
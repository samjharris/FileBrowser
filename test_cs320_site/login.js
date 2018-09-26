var message_active = false;
$("#theform").submit(function( event ) {
    event.preventDefault();
    console.log(message_active)
    if(!message_active)
    {
      $("#alertdiv").css("display", "block");
      $("#alertdiv").addClass("alert alert-danger")
      $("#alertdiv").append('<a href="#" id="close_me" class="close" data-dismiss="alert" aria-label="close">&times;</a>')
      $("#alertdiv").append("<strong>Incorrect!</strong> Wrong username or password.")
      $("#submit_btn").empty();
      $("#submit_btn").append('<i class="fa fa-refresh fa-spin"></i> Loading');
      $("#submit_btn").attr("disabled", true);
      message_active = true;
    }
  });

$(document).on("click", "#close_me", function(event) {
  event.preventDefault();
  $("#alertdiv").fadeOut("slow", function(){
    message_active = false;
    $("#alertdiv").removeClass();
    $("#alertdiv").empty();
    console.log(message_active)
  })
});

function getCurrentPageNumber()
{
  var url = window.location.href;
  if(url.includes("&page="))
  {
    var page_array = url.split("&page=");
    var right_side = page_array[1];//get what is on the right of the equal sign
    var num_array = [];

    for(let i = 0; i < right_side.length; i++)
    {
      var character = right_side[i];
      if(isNaN(character))
      {
        break;
      }
      else
      {
        num_array.push(character);
      }
    }

    return parseInt(num_array.join(""));
  }
  return -1;
}

var page_options = document.getElementById("page_options").children;
var page_number = getCurrentPageNumber();

for(let i = 0; i < page_options.length; i++)
{
  var page_option = page_options[i];
  if(parseInt(page_option.firstElementChild.textContent) == page_number)
  {
    page_option.classList.add("active");
  }
}

if(page_number <= 1)
{
  $('#previous').addClass("disabled");
}

$(document).on("click", function(event) {
  var clicked = event.target;
  if ($(clicked).parents('#page_options').length) 
  {
    var hope = $(clicked).hasClass("disabled");
    console.log(hope)
    if(!hope)
    {
      window.location = build_url(clicked.textContent);
    }
  } 
});

function build_url(page)
{
  var result = window.location.protocol + "//" + window.location.host + "/" + window.location.pathname + "?&page=";
  if(page == "Previous")
  {
    if(page_number <= 1)
    {
      result += (page_number-1);
    }
    else
    {
      result += 1;
    }
  }
  else if(page == "Next")
  {
    result += (page_number+1);
  }
  else
  {
    result += page;
  }
  return result;
}

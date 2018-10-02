$(document).on("dblclick", function(event)
{
  event.preventDefault();
  var target = $(event.target);
  if (target.parent('div#flexbox').length) 
  {
    alert('Double clicked a box');
  }
});
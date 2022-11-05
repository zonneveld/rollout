function command(action,value)
{
  const xhttp = new XMLHttpRequest();
  xhttp.onload = function() {

  }
  xhttp.open("POST",action,true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send(value);
}

function reload()
{
    command('servo','channel=0&angle=180')
}
function shoot()
{
    command('shoot','shoot=true')
}


// "coast":
// "forward":
// "backward":
// "brake":
// "left_turn":
// "right_turn":
// "rotate_clockwise":
// "rotate_counterclockwise":

function coast()
{
    command('drive','modus=coast');
}
function forward()
{
    command('drive','modus=forward');
}
function backward()
{
    command('drive','modus=backward');
}
function brake()
{
    command('drive','modus=brake');
}
function left_turn()
{
    command('drive','modus=left_turn');
}
function right_turn()
{
    command('drive','modus=right_turn');
}
function rotate_clockwise()
{
    command('drive','modus=rotate_clockwise');
}
function rotate_counterclockwise()
{
    command('drive','modus=rotate_counterclockwise');
}
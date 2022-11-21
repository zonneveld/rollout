function command(action,value)
{
  const xhttp = new XMLHttpRequest();
  xhttp.onload = function() {

  }
  xhttp.open("POST",action,true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send(value);
}

function servo_init()
{
    command('servo','channel=0&angle=180')
    command('servo','channel=1&angle=90')
}
function shoot()
{
    command('shoot','shoot=true')
}

function sweep_left()
{
    command('sweep', 'direction=1')
}

function sweep_right()
{
    command('sweep', 'direction=-1')
}

function sweep_stop()
{
    command('stopsweep', 'direction=0')
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

function snapshot()
{

    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        // fetch("/snapshots/snapshot.jpg", {cache: 'reload', mode: 'no-cors'})
        // .then(() => document.getElementById("snapshot_container").src = "/snapshots/snapshot.jpg")
        document.getElementById("snapshot_container").src = "/snapshots/snapshot.jpg?"+Math.floor(Math.random() * 100);
    }
    xhttp.open("POST",'snapshot',true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send('snapshot=true');
}

function logout()
{

    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
         window.location = "logout.html"
    }
    xhttp.open("GET",'logout',false,"log","out");
    xhttp.send();
}
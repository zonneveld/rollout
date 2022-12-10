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
    command('servo','channel=0&angle=0')
    command('servo','channel=1&angle=90')
}

function servo_do(channel,angle)
{
    command('servo',`channel=${channel}&angle=${angle}`)
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

function motor_do(channel,value)
{
    command('motor',`channel=${channel}&value=${value}`)
}

function write_to_display(text)
{
    command('display',`text=${text}`)
}

function write_input_to_display(id)
{
    write_to_display(document.getElementById(id).value)
}

function snapshot()
{
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
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
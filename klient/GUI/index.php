<?php
    if(isset($_COOKIE["username"]) && isset($_COOKIE["session"]) && isset($_COOKIE["monitor"]))
    {
        
    }
    else
    {
        header('Location: login.html');
    }
?>

<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>GUI</title>
        <script type="text/javascript" src="JS/CoreFunctions.js"></script>
    <body>
        Cześć <?php echo $_COOKIE["username"]?>!<br>
        Obecnie jesteś podłączony do monitora: <?php echo $_COOKIE["monitor"]?><br>
        <button type="button" onClick="logout()">wyloguj</button>
        <a href="subscription.php">lista subskrybcji</a>
        <a href="sensors.php">lista sensorów</a>
    </body>
</html>

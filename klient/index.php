<?php
    if(isset($_COOKIE["username"]) && isset($_COOKIE["monitor"]) && isset($_COOKIE["session"]))
    {
        
    }
    else
    {
        //echo "username=".$_COOKIE["username"]."monitor=".$_COOKIE["monitor"]."session=".$_COOKIE["session"];
        header('Location: login.html');
    }
?>

<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>GUI</title>
        <script type="text/javascript" src="JS/CoreFunctions.js"></script>
        <script type="text/javascript">
            function checkCookie()
            {
                if(readCookie("monitor") == null || readCookie("username") == null){
                    window.location = "login.html";
                }
            }
        </script>
    <body onLoad="checkCookie()">
        Cześć <?php if(isset($_COOKIE["username"])) echo $_COOKIE["username"]?>!<br>
        Obecnie jesteś podłączony do monitora: <?php if(isset($_COOKIE["monitor"])) echo $_COOKIE["monitor"]?><br>
        <button type="button" onClick="logout()">wyloguj</button>
        <a href="subscription.php">lista subskrybcji</a>
        <a href="sensors.php">lista sensorów</a>
    </body>
</html>

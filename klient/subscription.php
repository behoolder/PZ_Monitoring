<?php
include("checkLogin.php");
if(!checkLogin())
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
        <script type="text/javascript">
            var xmlhttp = createRequest();
            
            function getSubscriptionsResult()
            {
                if (this.readyState==4)
                {
                    if(this.status==200)
                    {
                        document.getElementById("TableBody").innerHTML = this.responseText;
                    }
                    else
                    {
                        var target = document.getElementById("Error");
                        target.innerHTML = "ERROR: <BR>"
                        target.innerHTML += this.status + " " + this.responseText;
                        target.style.visibility = "visible";
                    }
                }
            }
            function getSubscriptions()
            {
                var url = "Subscriptions/getSubscriptions.php?user=" + readCookie("username");
                xmlhttp.open("GET", url, true);
                xmlhttp.onreadystatechange = getSubscriptionsResult;
                xmlhttp.withCredentials = "true";
                xmlhttp.send();
            }
            function getRemoveResult()
            {
                if (this.readyState==4)
                {
                    if(this.status==200)
                    {
                        getSubscriptions();
                    }
                    else
                    {
                        var target = document.getElementById("Error");
                        target.innerHTML = "ERROR: <BR>"
                        target.innerHTML += this.status + " " + this.responseText;
                        target.style.visibility = "visible";
                    }
                }
            }
            function removeSubscription()
            {
                var url = "Subscriptions/removeSubscription.php?monitor=" + readCookie("monitor") + "&sid=";
                var inputs = document.getElementsByTagName("input");
                for(var i = 0; i < inputs.length; i++)
                {
                    if(inputs[i].checked == true)
                    {
                        url += inputs[i].value;
                        break;
                    }
                }
                xmlhttp.open("GET", url, true);
                xmlhttp.onreadystatechange = getRemoveResult;
                xmlhttp.withCredentials = "true";
                xmlhttp.send();
            }
            function showSubscription()
            {
                var sid = 0;
                var inputs = document.getElementsByTagName("input");
                for(var i = 0; i < inputs.length; i++)
                {
                    if(inputs[i].checked == true)
                    {
                        sid = parseInt(inputs[i].value);
                        break;
                    }
                }
                window.location = "Graph/graph.php?sid=" + sid;
            }
        </script>
    </head>
    <body onload ="getSubscriptions()">
        Cześć <?php echo $_COOKIE["username"]?>!<br>
        Obecnie jesteś podłączony do monitora: <?php echo $_COOKIE["monitor"]?><br>
        <a href="subscription.php">lista subskrybcji</a>
        <a href="sensors.php">lista sensorów</a>
        
        <div id ="Error"></div>
        <div id ="myDiv">
            <table id ="SubscrTables" border="1">
                <thead>
                    <tr>
                        <th></th>
                        <th>ID</th>
                        <th>sensor</th>
                        <th>metryka</th>
                    </tr>
                </thead>
                <tbody id ="TableBody">
                </tbody>
            </table>
            <button type="button" onClick="logout()">Wyloguj</button>
            <button type="button" onClick="removeSubscription()">Usuń</button>
            <button type="button" onClick="showSubscription()">Pokaż Wartość</button>
        </div>
    </body>
</html>

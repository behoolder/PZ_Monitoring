<!DOCTYPE html>
<html>
    <head>
        <title>GRAPH</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <script type="text/javascript" src="JS/CoreFunctions.js"></script>
        <script type="text/javascript">
            function getResult()
            {
                if (this.readyState==4)
                {
                    if(this.status==200)
                    {
                        var div = document.getElementById('graph');
                        div.innerHTML = this.responseText
                    }
                    else if(this.status==0)
                    {
                        var target = document.getElementById("error");
                        target.innerHTML = "ERROR: <BR>Network Error";
                    }
                    else
                    {
                        var target = document.getElementById("error");
                        target.innerHTML = "ERROR: <BR>"
                        target.innerHTML += this.status + " " + this.responseText;
                        target.style.visibility = "visible";
                    }
                }
            }
            function showValue(sid)
            {
                var xmlhttp = new createRequest();
                var url = "proxy/proxy.php?method=GET&url=";
                url += readCookie("monitor") + '/subscriptions/' + sid + '/';
                xmlhttp.open("GET", url, true);
                xmlhttp.onreadystatechange = getResult  ;
                xmlhttp.send();
            }
        </script>

    </head>
    <body>
        <button type="button" onClick="logout()">wyloguj</button>
        <a href="subscription.php">lista subskrybcji</a>
        <a href="sensors.php">lista sensorów</a>

        <?php
        if(!isset($_GET["sid"])) {
            echo 'dupa z Ciebie';
        } else {
            echo '<div id="sid'.$_GET["sid"].'" style="visibility: hidden" sid='.$_GET["sid"].'></div>';
        }
        ?>
        <div id ="error"></div>
        <div id ="graph">
            
        </div>
        <script type="text/javascript">
            <?php
            if(!isset($_GET["sid"])) {
                echo 'dupa z Ciebie';
            } else {
                echo 'setInterval("showValue('.$_GET["sid"].')", 1000)';
            }
            ?>
        </script>
    </body>
</html>
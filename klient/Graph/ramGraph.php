<?php
include("../checkLogin.php");
if(!checkLogin())
{
    header('Location: ../login.html');
}
?>

<!DOCTYPE html>
<html>
    <head>
        <title>GRAPH</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <script type="text/javascript" src="../JS/CoreFunctions.js"></script>
        <script type="text/javascript" src="../JS/jQuery.js"></script>
        <script type="text/javascript" src="../amcharts/amstock.js"></script>
        <script type="text/javascript">
            
            var chart;
            var data = [{
                    metric : '', 
                    value : 0
                }];
            
            AmCharts.ready(function(){
                    chart = new AmCharts.AmPieChart();
                    chart.dataProvider = data;
                    chart.titleField = "metric";
                    chart.valueField = "value";
                    chart.outlineColor = "#FFFFFF";
                    chart.outlineAlpha = 0.8;
                    chart.outlineThickness = 2;
                    
                    chart.write("graph");
                });
            function drawHDDChart(result)
            {
                data = [];
                var JSONObject = jQuery.parseJSON( result );
                for(var sensor in JSONObject)
                {
                    for(var ram in JSONObject[sensor])
                    {
                        data = [{
                            metric : "free",
                            value : JSONObject[sensor][ram].free
                        },{
                            metric : "used",
                            value : JSONObject[sensor][ram].used
                        }];
                    }
                }

                chart.dataProvider = data;
                chart.validateData();
            }
            function getResult()
            {
                if (this.readyState==4)
                {
                    if(this.status==200)
                    {
                        drawHDDChart(this.responseText);
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
                var url = "../Proxy/proxy.php?method=GET&url=";
                url += readCookie("monitor") + '/subscriptions/' + sid + '/';
                xmlhttp.open("GET", url, true);
                xmlhttp.withCredentials = "true";
                xmlhttp.onreadystatechange = getResult;
                xmlhttp.send();
            }
        </script>

    </head>
    <body onload ="showValue(<?php echo $_GET["sid"] ?>)">
        <a href="../subscription.php">lista subskrybcji</a>
        <a href="../sensors.php">lista sensorów</a>
        <div id="sidID" style="visibility: hidden"><?php echo $_GET["sid"] ?></div>
        <div id ="error"></div>
        <div id ="graph" style="width: 100%; height: 400px;"></div>
        <script type="text/javascript">
            <?php
            if(!isset($_GET["sid"])) {
                echo 'dupa z Ciebie';
            } else {
                echo 'setInterval("showValue('.$_GET["sid"].')", 10000);';
            }
            ?>
        </script>
    </body>
</html>
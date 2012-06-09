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
            
            var db = openDatabase("subscresults.db", "1.0", "Test", 10*1024*1024);
            var dropStatement = "drop table subscription_values";
            var insertStatement = "insert into subscription_values ('sid', 'type', 'value', 'timestamp') values (?,?,?, DATETIME('now'))";
            var deleteStatement = "delete from subscription_values where sid = ?";
            var selectStatement = "select * from subscription_values where sid = ?";
            var createStatement = "create table if not exists subscription_values (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, sid TEXT, value TEXT, timestamp DATETIME)";
            var chart;
            var data = [];
            
            //dropTable();
            
            AmCharts.ready(function(){
                    chart = new AmCharts.AmSerialChart();
                    chart.pathToImages = "../amcharts/images/";
                    chart.dataProvider = data;
                    chart.categoryField = "timestamp";
                    
                    var graph = new AmCharts.AmGraph();
                    graph.title = "red line";
                    graph.valueField = "system";
                    chart.addGraph(graph);
                    
                    chart.write("graph");
                });
            
            function onError(tx, error)
            {
                alert(error.message);
            }
            
            function dropTable()
            {
                db.transaction(function(tx) {
                    tx.executeSql(dropStatement, [], null, onError);
                });
            }
            function deleteRecords(sid)
            {
                db.transaction(function(tx) {
                    tx.executeSql(deleteStatement, [sid.toString()], null, onError);
                });
            }
            function drawCPUChart(tx, result)
            {
                var rows = result.rows;
                data = [];
                var temp;
                var array;
                
                if(rows.length <= 50)
                {
                    for(var i = 0; i < rows.length; i++)
                    {
                        temp = rows.item(i).value.split(';');
                        array = new Array();
                        for(var j = 0; j < temp.length; j++)
                            array.push(new Array(temp[j].split('=')[0], temp[j].split('=')[1]));

                        data.push({
                            id: rows.item(i).id,
                            system: array[0][1]
                        });
                    }
                }
                else
                {
                    for(var i = rows.length - 50; i < rows.length; i++)
                    {
                        temp = rows.item(i).value.split(';');
                        array = new Array();
                        for(var j = 0; j < temp.length; j++)
                            array.push(new Array(temp[j].split('=')[0], temp[j].split('=')[1]));

                        data.push({
                            id: rows.item(i).id,
                            system: array[0][1]
                        });
                    }
                }
                chart.dataProvider = data;
                chart.validateData();
            }
            
            function getSubscriptionValues()
            {
                var sid = document.getElementById("sidID").childNodes[0].nodeValue;
                db.transaction(
                    function(tx){
                        tx.executeSql(selectStatement, [sid], drawCPUChart, onError)
                    }
                );
            }
            function saveSubscription(json)
            {
                var JSONObject = jQuery.parseJSON( json );
                var result = "";
                var type = "";
                for(var hosts in JSONObject)
                {
                    if(typeof JSONObject[hosts].CPU != "undefined")
                    {
                        result = "system=" + JSONObject[hosts].CPU.system;
                        type = "CPU";
                    }
                    if(typeof JSONObject[hosts].RAM != "undefined")
                    {
                        result = "free=" + JSONObject[hosts].RAMfree + ";total=" + JSONObject[hosts].RAM.total + ";used=" + JSONObject[hosts].RAM.used;
                        type = "RAM";
                    }
                    if(typeof JSONObject[hosts].HDD != "undefined")
                    {
                        result = "free=" + JSONObject[hosts].RAMfree + ";total=" + JSONObject[hosts].RAM.total + ";used=" + JSONObject[hosts].RAM.used + ";name=" + JSONObject[hosts].RAM.name;
                        type = "HDD";
                    }
                }
                
                var sid = document.getElementById("sidID").childNodes[0].nodeValue;
                db.transaction(
                    function(tx){
                        tx.executeSql(createStatement, [], null, onError);
                        tx.executeSql(insertStatement, [sid, type, result], null, onError);
                    }
                );
                getSubscriptionValues();
            }
            function getResult()
            {
                if (this.readyState==4)
                {
                    if(this.status==200)
                    {
                        saveSubscription(this.responseText);
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
    <body onload="deleteRecords(<?php echo $_GET["sid"] ?>); showValue(<?php echo $_GET["sid"] ?>)">
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
                echo 'setInterval("showValue('.$_GET["sid"].')", 1000);';
            }
            ?>
        </script>
    </body>
</html>
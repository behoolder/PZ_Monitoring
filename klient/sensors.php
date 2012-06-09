<?php
include("checkLogin.php");
if(!checkLogin())
{
    //header('Location: login.html');
}
?>

<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>GUI</title>
        <script type="text/javascript" src="JS/CoreFunctions.js"></script>
        <script type="text/javascript" src="JS/PostSaveSubscription.js"></script>
        <script type="text/javascript" src="JS/jQuery.js"></script>
        <script type="text/javascript">
            var xmlhttp = createRequest();
            var http = createRequest();
            
            function logout()
            {
                eraseCookie("username");
                eraseCookie("monitor");
                window.location = "index.php"
            }
            function getSensorsResult()
            {
                if (this.readyState==4)
                {
                    if(this.status==200)
                    {
                        var metricFilter = document.getElementById("metric").value;
                        var sensorFilter = document.getElementById("sensor").value.toUpperCase();
                        var td;
                        var tag;
                        var input;
                        var target = document.getElementById("SensorBody");
                        target.innerHTML = '';
                        var jsonObject = jQuery.parseJSON(this.responseText);
                        var i = 0;
                        
                        for(var resource in jsonObject.resources)
                        {
                            if(metricFilter != "")
                            {
                                var found = false;
                                for(var j = 0; j < jsonObject.resources[resource].metrics.length; j++)
                                {
                                        var str = jsonObject.resources[resource].metrics[j];
                                        if(str.indexOf(metricFilter) != -1)
                                        {
                                            found = true;
                                            break;
                                        }
                                }
                                if(!found)
                                {
                                    continue;
                                }
                            }

                            if(sensorFilter != "")
                            {
                                var str = jsonObject.resources[resource].name.toUpperCase();
                                if(str.indexOf(sensorFilter) == -1)
                                    continue;
                            }

                            tag = document.createElement('tr');
                            tag.id = "SensorRow" + i;
                            input = document.createElement('input');
                            input.type = "radio";
                            input.name = "group";
                            input.value = "SensorRow" + i;
                            td = document.createElement('td');
                            td.appendChild(input)
                            tag.appendChild(td);
                            target.appendChild(tag);
                            var target1 = document.getElementById("SensorRow" + i);

                            jsonObject.resources[resource];
                            tag = document.createElement('td');
                            tag.id = "SensorColl" + i.toString();
                            tag.appendChild(document.createTextNode(
                                                                    jsonObject.resources[resource].address + ':' +
                                                                    jsonObject.resources[resource].port
                                                                    ));
                            target1.appendChild(tag);
                            tag = document.createElement('td');
                            tag.id = "SensorColl" + i.toString();
                            tag.appendChild(document.createTextNode(
                                                                    jsonObject.resources[resource].name
                                                                    ));
                            target1.appendChild(tag);

                            var option;
                            var select = document.createElement("select");
                            select.id = "SelectSensorRow" + i;
                            select.name = "SelectSensorRow" + i;;
                            select.size = 1;
                            for(var metric in jsonObject.resources[resource].metrics)
                            {
                                option = document.createElement("option");
                                option.appendChild(document.createTextNode(
                                                                            jsonObject.resources[resource].metrics[metric]
                                                                            ));
                                select.appendChild(option)
                            }
                            target1.appendChild(select);
                            i++;
                        }
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
            function getSubscribeResult()
            {
                if (this.readyState==4)
                {
                    if(this.status==200)
                    {
                        alert("Subskrypcja zapisana!");
                        window.location = "sensors.php";
                    }
                    else
                    {
                        var target = document.getElementById("Error");
                        target.innerHTML = "ERROR: <BR>"
                        target.innerHTML += http.status + " " + http.responseText;
                        target.style.visibility = "visible";
                    }
                }
            }
            /*function parseSensorsList(string)
            {
                while(string.indexOf(' ') != -1)
                    string = string.replace(' ', '');
                while(string.indexOf('{') != -1)
                    string = string.replace('{', '');
                while(string.indexOf('}') != -1)
                    string = string.replace('}', '');
                while(string.indexOf('(') != -1)
                    string = string.replace('(', '');
                while(string.indexOf(')') != -1)
                    string = string.replace(')', '');
                while(string.indexOf('"') != -1)
                    string = string.replace('"', '');

                var tempArray = string.split(',');
                var tempArray1 = new Array();
                var array = new Array();
                
                if(string == "")
                    return array;

                for(var i = 0; i < tempArray.length; i=i+2)
                    tempArray1.push(tempArray[i] + ',' + tempArray[i+1]);

                for(var i = 0; i < tempArray1.length; i++)
                {
                    array.push(tempArray1[i].split(':'));
                }
                for(var i = 0; i < array.length; i++)
                {
                    for(var j = 0; j < array[i].length; j=j+2)
                    {
                        array[i][j] = array[i][j].split(',')[0] + ':' + array[i][j].split(',')[1];
                    }
                }
                return array;
            }*/
            function getSensors()
            {
                var url = "Proxy/proxy.php?method=GET&url=";
                    url += readCookie("monitor") + '/resources/';
                xmlhttp.open("get", url, true);
                xmlhttp.onreadystatechange = getSensorsResult;
                xmlhttp.withCredentials = "true";
                xmlhttp.send("");
            }
            function subscribe()
            {
                var url = "Subscriptions/saveSubscription.php?url="
                url += readCookie("monitor") + '/subscribe/';
                var inputs = document.getElementsByTagName("input");
                var sensor, ip, port, metric, select, cpu = 0, ram = 0, hdd = 0;
                for(var i = 0; i < inputs.length; i++)
                {
                    if(inputs[i].checked == true)
                    {
                        sensor = document.getElementById(inputs[i].value);
                        ip = sensor.childNodes[1].firstChild.nodeValue.split(":")[0];
                        port = sensor.childNodes[1].firstChild.nodeValue.split(":")[1];
                        select = document.getElementById("Select" + inputs[i].value);
                        metric = select.options[select.selectedIndex].value;
                        break;
                    }
                }
                
                
                switch (metric)
                {
                    case 'CPU':
                        cpu = 1;
                        break;
                    case 'HDD':
                        hdd = 1;
                        break;
                    case 'RAM':
                        ram = 1;
                        break;
                    default:
                        cpu = 0; ram = 0; hdd = 0;
                }
                
                var params = "host=" + ip + "&port=" + port + "&cpu=" + cpu + "&hdd=" + hdd + "&ram=" + ram;
                url += "&postdata=" + encodeURIComponent(params); 
                url += "&metric=" + metric + "&sensor=" + ip + ":" + port;
                http.open("GET", url, true);
                http.onreadystatechange = getSubscribeResult;
                http.send();
            }
            function filter()
            {
                var dupa = 1;
            }
            
        </script>
    </head>
    <body onload ="getSensors()">
        Cześć <?php echo $_COOKIE["username"]?>!<br>
        Obecnie jesteś podłączony do monitora: <?php echo $_COOKIE["monitor"]?><br>
        <a href="subscription.php">lista subskrybcji</a>
        <a href="sensors.php">lista sensorów</a>
        <div id ="Error"></div>
        <div id="Filter">
            Zasób: 
            <input id="sensor" type="text" name="sensor">
            Metryka:
            <input id="metric" type="text" name="metric">
            <button type="button" onClick="getSensors()">Filtruj</button>
        </div>

        <div id ="myDiv">
            <table id ="SensorTables" border="1">
                <thead>
                    <tr>
                        <th></th>
                        <th>IP:port</th>
                        <th>Zasób</th>
                        <th>Metryka</th>
                    </tr>
                </thead>
                <tbody id="SensorBody">
                </tbody>
            </table>
            <button type="button" onClick="logout()">Wyloguj</button>
            <button type="button" id="subscribe" onClick="subscribe()">Subskrybuj</button>
        </div>
    </body>
</html>

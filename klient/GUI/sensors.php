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
        <script type="text/javascript" src="JS/PostSaveSubscription.js"></script>
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
                        var tag;
                        var input;
                        var target = document.getElementById("SensorBody");
                        var array = parseSensorsList(this.responseText);
                        for(var i = 0; i < array.length; i++)
                        {
                            tag = document.createElement('tr');
                            tag.id = "SensorRow" + i;
                            input = document.createElement('input');
                            input.type = "radio";
                            input.name = "group";
                            input.value = "SensorRow" + i;
                            tag.appendChild(input);
                            target.appendChild(tag);
                            var target1 = document.getElementById("SensorRow" + i);
                            for(var j = 0; j < array[i].length; j++)
                            {
                                tag = document.createElement('td');
                                tag.id = "SensorColl" + i.toString() + j;
                                tag.appendChild(document.createTextNode(array[i][j]));
                                target1.appendChild(tag);
                            }
                            target1.appendChild(createComboBox("SelectSensorRow" + i));
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
                        saveSubscription(this.responseText);
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
            function parseSensorsList(string)
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
            }
            function getSensors()
            {
                var url = readCookie("monitor") + '/sensors/';
                xmlhttp.open("get", url, true);
                xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                xmlhttp.onreadystatechange = getSensorsResult;
                xmlhttp.withCredentials = "true";
                xmlhttp.send("");
                //ip=127.0.0.1&port=1001&cpu=1&ram=0&hdd=0
            }
            function subscribe()
            {
                var url = "proxy/proxy.php?method=POST&url="
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
                http.open("GET", url, true);
                http.onreadystatechange = getSubscribeResult;
                //http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                //http.withCredentials = "true";
                http.send();
            }
            function createComboBox(id)
            {
                var option;
                var select = document.createElement("select");
                select.id = id;
                select.name = id;
                select.size = 1;
                option = document.createElement("option");
                option.appendChild(document.createTextNode("HDD"));
                select.appendChild(option)
                option = document.createElement("option");
                option.appendChild(document.createTextNode("RAM"));
                select.appendChild(option)
                option = document.createElement("option");
                option.appendChild(document.createTextNode("CPU"));
                select.appendChild(option)
                return select
            }
            
        </script>
    </head>
    <body onload ="getSensors()">
        Cześć <?php echo $_COOKIE["username"]?>!<br>
        Obecnie jesteś podłączony do monitora: <?php echo $_COOKIE["monitor"]?><br>
        <button type="button" onClick="logout()">wyloguj</button>
        <a href="subscription.php">lista subskrybcji</a>
        <a href="sensors.php">lista sensorów</a>
        <div id ="Error"></div>
        <div id ="myDiv">
            <table id ="SensorTables" border="1">
                <thead>
                    <tr>
                        <th></th>
                        <th>ip:port</th>
                        <th>sensor</th>
                        <th>metryka</th>
                    </tr>
                </thead>
                <tbody id="SensorBody">
                </tbody>
            </table>
            <button type="button" id="subscribe" onClick="subscribe()">Subskrybuj</button>
        </div>
    </body>
</html>

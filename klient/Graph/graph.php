<?php

include("../checkLogin.php");
if(!checkLogin())
{
    header('Location: login.html');
}

if(isset($_GET["sid"]))
{
    $sid = $_GET["sid"];
}

$fileName = '../Subscriptions/subscriptions.db';
$exists = file_exists($fileName);
$db = new SQLite3($fileName);
if(!$exists)
{
    $db->close();
}
$query = "SELECT metric FROM subscriptions WHERE id = '".$sid."'";
$metric = $db->querySingle($query);
$metric = strtoupper($metric);
if(!$metric)
{
    $message = $db->lastErrorMsg();
}
switch($metric)
{
    case 'CPU':
        header('Location: cpuGraph.php?sid='.$sid);
        break;
    case 'HDD':
        header('Location: hddGraph.php?sid='.$sid);
        break;
    case 'RAM':
        header('Location: ramGraph.php?sid='.$sid);
        break;
    default:
        break;
}


?>
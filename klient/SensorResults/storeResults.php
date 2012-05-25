<?php
$temp = '{"AJAX": {"CPU": {"system": "15"}}}';
$sid = 13;
include 'results.php';

function storeResult($result, $sid)
{
    $fileName = 'subscriptionValues.db';
    $exists = file_exists($fileName);
    $db = new SQLite3($fileName);
    $tableCreate = @"CREATE TABLE subscription_values 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
        type TEXT,
        sid INTEGER, 
        value TEXT, 
        timestamp DATETIME)";
    if(!$exists)
    {
        $db->exec($tableCreate);
    }
    $insert = "INSERT INTO subscription_values (sid, value, timestamp) VALUES('".$sid."','".$result->getResult()."','".$result->timestamp."')";
    $result = $db->exec($insert);
    $db->close(); 
}

//echo $_GET["result"];
//$data = json_decode($_GET["result"]);
$data = json_decode($temp);

foreach($data as $host)
{
    if(property_exists($host, 'CPU'))
    {
        $result = new CPU($host->CPU->system, "");//$host->CPU->user);
    }
    if(property_exists($host, 'RAM'))
    {
        $result = new RAM($host->RAM->free, $host->RAM->used, $host->RAM->total);
    }
    if(property_exists($host, 'HDD'))
    {
        $result = new HDD($host->HDD->free, $host->HDD->used, $host->HDD->total, $host->HDD->name);
    }
    
    storeResult($result, $sid);
}
?>
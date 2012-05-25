<?php

function removeResults($sid)
{
    $fileName = 'subscriptionValues.db';
    $exists = file_exists($fileName);
    $db = new SQLite3($fileName);
    if(!$exists)
    {
        return;
    }
    $query = "SELECT * FROM subscription_values WHERE sid = ".$sid;
    $result = $db->query($query);
    $array = $result->fetchArray();
    if($array == false)
    {
        $delete = "DELETE FROM subscription_values WHERE ID = ".$sid;
        $db->exec($delete);
    }
    $db->close(); 
}

if(isset($_GET["sid"]))
{
    $sid = $_GET["sid"];
    removeResults($sid);
}
?>
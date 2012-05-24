<?php
//$subscr = json_decode('{"Maciek": [{"metric": ["cpu"], "sensor": ["127.0.0.1", "1002"], "id": 1}]}');
//$user = 'Maciek';

class Subscription
{
    public $id, $sensor, $metric;
    
    public function __construct($iId, $iSensor, $iMetric)
    {
        $this->id = $iId;
        $this->sensor = $iSensor;
        $this->metric = $iMetric;
    }
}

function saveSubscription($user, $subscription)
{
    $fileName = 'subscriptions.db';
    $exists = file_exists($fileName);
    $db = new SQLite3($fileName);
    $tableCreate = "CREATE TABLE subscriptions (id INTEGER PRIMARY KEY, user TEXT, sensor TEXT, metric TEXT)";
    if(!$exists)
    {
        $db->exec($tableCreate);
    }
    $query = "SELECT * FROM subscriptions WHERE id = ".$subscription->id;
    $result = $db->query($query);
    $array = $result->fetchArray();
    if($array == false)
    {
        $insert = "INSERT INTO subscriptions VALUES (".$subscription->id.",'".$user."','".$subscription->sensor."','".$subscription->metric."')";
        //echo $insert;
        $db->exec($insert);
    }
    $db->close(); 
}

if(isset($_GET['subscr']))
{
    $temp = $_GET['subscr'];
    $subscr = json_decode($temp);
}

if(isset($_GET['user']))
{
    $user = $_GET['user'];
    echo $user;
}


foreach($subscr->$user as $subscription)
{
    $sub = new Subscription($subscription->id, $subscription->sensor, $subscription->metric[0]);
    saveSubscription($user, $sub);
}
?>

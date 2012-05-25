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

function removeSubscription($sid)
{
    $fileName = 'subscriptions.db';
    $exists = file_exists($fileName);
    $db = new SQLite3($fileName);
    $tableCreate = "CREATE TABLE subscriptions (id INTEGER PRIMARY KEY, user TEXT, sensor TEXT, metric TEXT)";
    if(!$exists)
    {
        $db->exec($tableCreate);
    }
    $query = "SELECT * FROM subscriptions WHERE id = ".$sid;
    $result = $db->query($query);
    $array = $result->fetchArray();
    if($array == false)
    {
        $delete = "DELETE FROM subscriptions WHERE ID = ".$sid;
        $db->exec($delete);
    }
    $db->close(); 
}

if(isset($_GET['sid']))
{
    $sid = $_GET['sid'];
}

if(isset($_GET['monitor']))
{
    $monitor = $_GET['monitor'];
}

$url = $monitor."/subscriptions/".$sid."/";
removeSubscription($sid);
$r = new HttpRequest($url, HttpRequest::METH_DELETE);
//$r->addHeaders(array("cookie" => "session=".$_COOKIE["session"]));
$responseMessage = $r->send();
$responseMessage->send();
?>

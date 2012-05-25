<?php
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
    $delete = "DELETE FROM subscriptions WHERE id = ".$sid;
    $res = $db->exec($delete);
    if($res == false)
    {
        $message = $db->lastErrorMsg();
    }
    $db->close();
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
    if($result)
    {
        $array = $result->fetchArray();
        if(!$array)
        {
            $insert = "INSERT INTO subscriptions VALUES (".$subscription->id.",'".$user."','".$subscription->sensor."','".$subscription->metric."')";
            $result = $db->exec($insert);
        }
    }
    $db->close(); 
}

function getSubscriptions($user)
{
    $array = new ArrayObject();
    $arrayToRemove = new ArrayObject();
    $fileName = 'subscriptions.db';
    $exists = file_exists($fileName);
    $db = new SQLite3($fileName);
    if(!$exists)
    {
        $db->close();
        return $array;
    }
    $query = "SELECT * FROM subscriptions WHERE user = '".$user."'";
    $result = $db->query($query);
    if($result)
    {
        while($res = $result->fetchArray(SQLITE3_ASSOC))
        {
            $sid = $res["id"];
            $url = $_COOKIE["monitor"]."/subscriptions/".$sid;
            $r = new HttpRequest($url, HttpRequest::METH_GET);
            $responseMessage = $r->send();
            if($responseMessage->getResponseCode() ==  404)
            {
                $arrayToRemove->append($sid);
            }
            else
            {
                $array->append($res);
            }
            /*$url = $_COOKIE["monitor"]."/subscription_list/";
            $r = new HttpRequest($url, HttpRequest::METH_POST);
            //$r->setBody('{"sid" : "'.$sid.'"}');
            $r->setBody("sid=".$sid);
            $responseMessage = $r->send();
            //$message = $r->getRawPostData();
            $json = json_decode($responseMessage->getBody());
            if($json->available == 'true')
            {
                $array->append($res);
            }
            else
            {
                $arrayToRemove->append($sid);
            }*/
            
        }
    }
    $db->close(); 
    
    foreach($arrayToRemove as $sid)
    {
        removeSubscription($sid);
    }
    return $array;
}
?>

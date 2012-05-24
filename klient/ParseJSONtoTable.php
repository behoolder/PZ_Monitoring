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

if(isset($_GET['subscr']))
{
    $temp = $_GET['subscr'];
    $subscr = json_decode($temp);
}

if(isset($_GET['user']))
{
    $user = $_GET['user'];
}

$sub = array();

foreach($subscr->$user as $subscription)
{
    array_push($sub, new Subscription(
            $subscription->id, 
            $subscription->sensor[0].':'.$subscription->sensor[1], 
            $subscription->metric[0]));
}

$string = '';
$tr = '<tr>';
$tr_close = '</tr>';
$td = '<td>';
$td_close = '</td>';
$input = '<input type="radio" name="group" value="';

foreach($sub as $subscription)
{
    $string.=$tr;
    $string.=$td;
    $string.=$input.$subscription->id.'">';
    $string.=$td_close;
    $string.=$td;
    $string.=$subscription->id;
    $string.=$td_close;
    $string.=$td;
    $string.=$subscription->sensor;
    $string.=$td_close;
    $string.=$td;
    $string.=$subscription->metric;
    $string.=$td_close;
    $string.=$tr_close;
}

$responseMessage = new HttpMessage();
$responseMessage->setType(httpmessage::TYPE_RESPONSE);
$responseMessage->setBody($string);
$responseMessage->setResponseCode(200);
$responseMessage->send();

?>

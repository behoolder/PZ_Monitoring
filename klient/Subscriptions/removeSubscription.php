<?php
//$subscr = json_decode('{"Maciek": [{"metric": ["cpu"], "sensor": ["127.0.0.1", "1002"], "id": 1}]}');
//$user = 'Maciek';

include('subscriptionClass.php');

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

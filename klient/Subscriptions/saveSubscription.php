<?php
include('subscriptionClass.php');

$url = $_COOKIE["monitor"]."/subscribe/";
$r = new HttpRequest($url, HttpRequest::METH_POST);
$r->setBody($_GET['postdata']);
$responseMessage = $r->send();
$subscr = json_decode($responseMessage->getBody());
$id = $subscr->id;

if(isset($_GET["metric"]))
{
    $metric = $_GET["metric"];
}

if(isset($_GET["sensor"]))
{
    $sensor = $_GET["sensor"];
}

if(isset($_COOKIE["username"]))
{
    $user = $_COOKIE["username"];
}

$sub = new Subscription($id, $sensor, $metric);
saveSubscription($user, $sub);

?>

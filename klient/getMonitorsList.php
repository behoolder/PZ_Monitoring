<?php
$monitors = 'monitors';
$url = $_GET["catalog"];
$r = new HttpRequest($url, HttpRequest::METH_GET);
$responseMessage = new HttpMessage();
$body = "";

try {
    $temp = $r->send()->getBody();
} catch (HttpException $ex)
{
    $responseMessage->setType(HttpMessage::TYPE_RESPONSE);
    $responseMessage->setBody($ex->getMessage());
    $responseMessage->setResponseCode(404);
    $responseMessage->send();
    exit();
}
$body = json_decode($temp);
$monitorsList = array();

foreach($body->$monitors as $monitor)
{
    array_push($monitorsList, $monitor->address.':'.$monitor->port);
}

foreach($monitorsList as $monitor)
{
    echo $monitor;
    echo';';
}
?>
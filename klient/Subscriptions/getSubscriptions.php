<?php
include('subscriptionClass.php');

if(isset($_GET["user"]))
{
    $user = $_GET["user"];
}

$subscriptionList = getSubscriptions($user);


$string = '';
$tr = '<tr>';
$tr_close = '</tr>';
$td = '<td>';
$td_close = '</td>';
$input = '<input type="radio" name="group" value="';

foreach($subscriptionList as $subscription)
{
    $string.=$tr;
    $string.=$td;
    $string.=$input.$subscription["id"].'">';
    $string.=$td_close;
    $string.=$td;
    $string.=$subscription["id"];
    $string.=$td_close;
    $string.=$td;
    $string.=$subscription["sensor"];
    $string.=$td_close;
    $string.=$td;
    $string.=$subscription["metric"];
    $string.=$td_close;
    $string.=$tr_close;
}

$responseMessage = new HttpMessage();
$responseMessage->setType(httpmessage::TYPE_RESPONSE);
$responseMessage->setBody($string);
$responseMessage->setResponseCode(200);
$responseMessage->send();
?>

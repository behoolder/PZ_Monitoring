<?php

function checkLogin()
{
    if(!(isset($_COOKIE["username"]) && isset($_COOKIE["monitor"]) && isset($_COOKIE["session"])))
    {
        return false;
    }
    
    $url = $_COOKIE["monitor"].'/subscription_list/';
    $r = new HttpRequest($url, HttpRequest::METH_GET);
    $responseMessage = $r->send();
    if($responseMessage->getResponseCode() == 404)
    {
        return false;
    }
    
    $json = json_decode($responseMessage->getBody());
    if(property_exists($json, "error"))
    {
        return false;
    }
    return true;
}

?>

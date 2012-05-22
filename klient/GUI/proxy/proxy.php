<?php
if(!isset($_GET['url']))
{
    echo "Error: Nie podales url";
    exit();
}
if(!isset($_GET['method']))
{
    echo "Error: Nie podales metody";
    exit();
}
/*if(!isset($_COOKIE["session"]))
{
    echo "Error: Nie jesteś zalogowany";
    exit();
}*/

$responseMessage = new HttpMessage();

switch(strtolower($_GET['method']))
{
    case 'get':
        $url = $_GET['url'];
        $r = new HttpRequest($url, HttpRequest::METH_GET);
        try {
            $responseMessage = $r->send();
            $responseMessage->send();
        } catch (HttpException $ex)
        {
            $responseMessage->setType(HttpMessage::TYPE_RESPONSE);
            $responseMessage->setBody($ex->getMessage());
            $responseMessage->setResponseCode(404);
            $responseMessage->send();
        }
        break;
    
    case 'post':
        if(!isset($_GET['postdata']))
        {
            echo "Error: Niepoprawny POST";
            exit();
        }
        $url = $_GET['url'];
        $r = new HttpRequest($url, HttpRequest::METH_POST);
        $r->setBody($_GET['postdata']);
        try {
            $responseMessage = $r->send();
            $responseMessage->send();
        } catch (HttpException $ex)
        {
            $responseMessage->setType(HttpMessage::TYPE_RESPONSE);
            $responseMessage->setBody($ex->getMessage());
            $responseMessage->setResponseCode(404);
            $responseMessage->send();
        }
        
        break;
    case 'delete':
        $url = $_GET['url'];
        $r = new HttpRequest($url, HttpRequest::METH_DELETE);
        try {
            $responseMessage = $r->send();
            $responseMessage->send();
        } catch (HttpException $ex)
        {
            //echo $ex->getMessage();
            $responseMessage->setType(HttpMessage::TYPE_RESPONSE);
            $responseMessage->setBody($ex->getMessage());
            $responseMessage->setResponseCode(404);
            $responseMessage->send();
        }
        break;
    default:
        echo "Error: Niepoprawna metoda";
        exit();
}
?>
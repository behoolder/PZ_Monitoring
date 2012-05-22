var xmlhttprequest = createRequest();

function saveSubscription(string)
{
    var xmlhttprequest = createRequest();
    var user = readCookie("username");
    var params = "user=" + user + "&subscr=" + string;
    var url = "SaveSubscription.php?" + params;
    xmlhttprequest.open("GET", url, true);
    xmlhttprequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttprequest.onreadystatechange = getSubscriptionResult;
    xmlhttprequest.withCredentials = "true";
    xmlhttprequest.send("");

}

function getSubscriptionResult()
{
    if (this.readyState==4)
    {
        if(this.status==200)
        {
            alert("Subskrypcja zapisana!")
        }
        else
        {
            var target = document.getElementById("Error");
            target.innerHTML = "ERROR: <BR>"
            target.innerHTML += this.status + " " + this.responseText;
            target.style.visibility = "visible";
        }
    }
}

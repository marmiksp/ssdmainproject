var list_of_msgs = []
var messages = document.querySelector('.message-list')
var btn = document.querySelector('#sendbtn')
var input = document.querySelector('input')
var userid = document.getElementById("userid")
var teamid = document.getElementById("teamid")

btn.addEventListener('click', sendMessage) 
input.addEventListener('keyup', function(e){ if(e.key === "Enter") sendMessage() })



///////////////////////////////////
/*DELETE THIS , JUST FOR TESTING */
// var testbtn = document.querySelector('.testbtn')
// testbtn.addEventListener('click', test)
function test()
{
   let msg1= {FROM:"SERVER", MESSAGE:"Hi friend. Its me server. Hi friend. Its me server. Hi friend. Its me server. Hi friend. Its me server. Hi friend. Its me server"};
   list_of_msgs.push(msg1);
   msg_from_server(msg1);
   
   console.log(list_of_msgs);

}
////////////////////////////////



//client logic

function sendMessage()
{
   var msg = input.value;
   /* also add logic to send this message to server here */
	 let msg1= {"FROM":"ME", "MESSAGE":msg};
	 let msg2= {FROM:"ME", MESSAGE:msg, TEAMID:teamid.innerHTML, USERID:userid.innerHTML};

   input.value = ''
   //writeLineclient(msg)
   ///msg_from_client(msg2);
   
   console.log(list_of_msgs);

   console.log(userid.innerHTML);
   
   
   $.getJSON("/catchmsg", {MESSAGE:JSON.stringify(msg2)}).done(function(data) {
    console.log(data.result);
    allmsg = data.result;
   //  list_of_msgs
   if(list_of_msgs.length != allmsg.length)
   {
      console.log("IN");
      st = list_of_msgs.length
      console.log(allmsg);
      console.log(list_of_msgs);
      for(var i=st;i<allmsg.length;i++)
      {
         let msg2= {FROM:"USERID ["+allmsg[i][1]+"]", MESSAGE:allmsg[i][2]}; 
         msg_from_server(msg2);
      }

      list_of_msgs = allmsg;
   }
    
    });
   
}
// setInterval(function(){ fetchmessages(); }, 2000);
function fetchmessages()
{
   let msg2= {TEAMID:teamid.innerHTML, USERID:userid.innerHTML};
   $.getJSON("/fetchmsg", {MESSAGE:JSON.stringify(msg2)}).done(function(data) {
      // console.log(data.result);
      allmsg = data.result;
      console.log("1");
     //  list_of_msgs
     if(list_of_msgs.length != allmsg.length)
     {
  
        st = list_of_msgs.length
  
        for(var i=st;i<allmsg.length;i++)
        {
           let msg2= {FROM:"USERID ["+allmsg[i][1]+"]", MESSAGE:allmsg[i][2]}; 
           msg_from_server(msg2);
        }
  
        list_of_msgs = allmsg;
     }


      });
}

function msg_from_client(e) //This function take json formatted message from server and displays it
{
   var msg = e.data ? JSON.parse(e.data) : e;
   writeLineclient(`${msg.FROM}: ${msg.MESSAGE}`)
}
function writeLineclient(text)
{
   var message = document.createElement('li')
   message.classList.add('message-item', 'item-primary')
   //message.innerHTML = 'Me: ' + text
   message.innerHTML = text
   messages.appendChild(message)
   messages.scrollTop = messages.scrollHeight;
}



//server msg recieved logic

function msg_from_server(e) //This function take json formatted message from server and displays it
{
   var msg = e.data ? JSON.parse(e.data) : e;
   writeLineserver(`${msg.FROM}`,` ${msg.MESSAGE}`)
}
function writeLineserver(from,msg)
{
  console.log(from)
   var message = document.createElement('li')
   message.classList.add('message-item', 'item-secondary')
   message.innerHTML = '<b style="color:white; border-radius:4px; padding:4px; background-color:green; ">'+from+'</b>  <i style="color:white;"> '+msg+'</i>';
   messages.appendChild(message)
   messages.scrollTop = messages.scrollHeight;
}









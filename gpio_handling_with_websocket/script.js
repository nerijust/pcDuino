var sock = null;
var wsuri = "ws://192.168.1.4:9000";
 
window.onload = function() {
 
    sock = new WebSocket(wsuri);
 
    sock.onopen = function() {
        console.log("connected to " + wsuri);
		sock.send("refresh");
        }
 
        sock.onclose = function(e) {
            console.log("connection closed (" + e.code + ")");
        }
 
        sock.onmessage = function message(e) {
			console.log("message received: " + e.data);
			write(e);
			}
        };

	function send(id){
		 
		var str = id;
		var gpio = str.split("myonoffswitch");
			
		if (document.getElementById(id).checked == true){
			var status = "1";
			}

		else {
			status = "0";
			}
			
		sock.send(gpio[1]+":"+status);
	};
		
	function write(e){
		
		var str = e.data;
		var myonoffswitch = str.split(":");
		var id ="myonoffswitch"+myonoffswitch[0];
		
		if (myonoffswitch[1] == "0"){
			document.getElementById(id).checked = false;
			}
			
		if(myonoffswitch[1] == "1"){
			document.getElementById(id).checked = true;
			}
	};	

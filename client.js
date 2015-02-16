var token = null;	//Using LocalStorage for set

//Display page view															
displayView = function(){ 							
// the code required to display a view
	token = JSON.parse(localStorage.getItem("token"));
	
	if(token == null) { //display welcomeview			//READ token from storage
		document.getElementById("welcomecontent").innerHTML = document.getElementById("welcomeview").innerHTML;	
		document.getElementById("profilecontent").innerHTML = "";
		
	} else { //display profileview
		document.getElementById("welcomecontent").innerHTML = "";	
		document.getElementById("profilecontent").innerHTML = document.getElementById("profileview").innerHTML;	
		selected(document.getElementById("homeitem"));
	}
};

//Window onload											
window.onload = function(){
	displayView();
};

//Show message element for 3 sec
var showErrorMessage = function(element) {
	setTimeout(function(){	//timer for showing errormessage only in 3sec
					document.getElementById(element).style.color = "white";	
	}, 3000);
}

//Account panel	
var changePassword = function(formData) {
	var oldpw = formData.oldpw.value;
	var newpw = formData.newpw.value;
	var newrpw = formData.newrpw.value;

	if(newpw == newrpw) {
		var serverResponse = serverstub.changePassword(token, oldpw, newpw);
		if(serverResponse.success) {
			document.getElementById("accErrorText").style.color = "green";
		}
		else {
			document.getElementById("accErrorText").style.color = "red";
		}
		document.getElementById("accErrorText").innerHTML = serverResponse.message;
	}
	else {
			document.getElementById("accErrorText").style.color = "red";
			document.getElementById("accErrorText").innerHTML = "New password dont match";
	}
	//clean up
	formData.newrpw.value = "";
	formData.newpw.value = "";
	formData.oldpw.value = "";
	
	showErrorMessage("accErrorText");
}
var signOut = function() {	
	var serverResponse = serverstub.signOut(token);
	localStorage.setItem("token", JSON.stringify(null));
	displayView();
}

//Browse panel	
var browseUser = function(formData){
	var user = formData.search.value;
	var userData = serverstub.getUserDataByEmail(token, user);
	
	if(userData.success) {
		document.getElementById("browsepanel").style.display = "none";
		document.getElementById("browseuser").style.display = "block";
		
		updatePersonalInfo(userData.data, false);	
				
	} else {
		document.getElementById("browsePanelError").style.color = "red";
		document.getElementById("browsePanelError").innerHTML = userData.message;
	}
	showErrorMessage("browsePanelError");	
}  

//Update Personal info	
var updatePersonalInfo = function(userData, home) {
	if(home){
		document.getElementById("homeEmail").innerHTML = userData.email;
		document.getElementById("homeFname").innerHTML = userData.firstname;
		document.getElementById("homeLname").innerHTML = userData.familyname;
		document.getElementById("homeGender").innerHTML = userData.gender;
		document.getElementById("homeCity").innerHTML = userData.city;
		document.getElementById("homeCountry").innerHTML = userData.country;
		
	} else {
		document.getElementById("userEmail").innerHTML = userData.email;
		document.getElementById("userFname").innerHTML = userData.firstname;
		document.getElementById("userLname").innerHTML = userData.familyname;
		document.getElementById("userGender").innerHTML = userData.gender;
		document.getElementById("userCity").innerHTML = userData.city;
		document.getElementById("userCountry").innerHTML = userData.country;	
	}	
	refreshWall(home);	//When loading a home/user page always refresh Wall.	
} 

//Refresh wall
var refreshWall = function(home) {
		var userMessages = "";
		
		if(home) {
			userMessages = serverstub.getUserMessagesByToken(token);

			if(userMessages.success) {
				updateWall(userMessages.data, home); 
			} else{
				document.getElementById("homeError").style.color = "red";
				document.getElementById("homeError").innerHTML = userMessages.message;
				showErrorMessage("homeError");
			}
		}				
		else {		//Update user wall	
			userMessages = serverstub.getUserMessagesByEmail(token, document.getElementById("userEmail").innerHTML);
			
			if(userMessages.success) {
				updateWall(userMessages.data, home); 
			} else {
				document.getElementById("browseError").style.color = "red";
				document.getElementById("browseError").innerHTML = userMessages.message;
				showErrorMessage("browseError");
			}	
		}		
		
} 
//Post to wall
var postWall = function(formData, home){	
	var serverResponse = "";
	if(home) {
		serverResponse = serverstub.postMessage(token,formData.msg.value, null);
		formData.msg.value = "";
		
		if(serverResponse.success) {
			document.getElementById("homeError").style.color = "green";
		} else {
			document.getElementById("homeError").style.color = "red";
		}
		
		document.getElementById("homeError").innerHTML = serverResponse.message;	
		showErrorMessage("homeError");
	
	} else {
		serverResponse = serverstub.postMessage(token, formData.msgUser.value, document.getElementById("userEmail").innerHTML);	
		formData.msgUser.value = "";
		
		if(serverResponse.success) {
			document.getElementById("browseError").style.color = "green";
		} else {
			document.getElementById("browseError").style.color = "red";		
		}
		
		document.getElementById("browseError").innerHTML = serverResponse.message;
		showErrorMessage("browseError");
	}
}
//Print out user messages on wall
var updateWall = function(messages, home) { 
	var msgs = "";
	
	for(var i = 0; i<messages.length; i++) { 
		msgs += "From: " + messages[i].writer+"\n" + messages[i].content +"\n\n";
	}   
	
	if(home) {
		document.getElementById("homeWall").innerHTML = msgs;
	}
	else {
		document.getElementById("userWall").innerHTML = msgs;
	}
} 

//Top menu			
var selected = function(item){
    item.style.backgroundColor = "purple";
    for (var i = 0 ; i <  item.parentNode.childNodes.length ; ++i){
        if (item.parentNode.childNodes[i].nodeType == Node.ELEMENT_NODE && item.parentNode.childNodes[i].innerHTML != item.innerHTML)
            item.parentNode.childNodes[i].style.backgroundColor = "pink";
    }

		document.getElementById("browseuser").style.display = "none";
		
    if(item.innerHTML == "<h3>home</h3>"){		
		document.getElementById("homepanel").style.display = "block";
		document.getElementById("browsepanel").style.display = "none";
		document.getElementById("accountpanel").style.display = "none";  
		
	   updatePersonalInfo(serverstub.getUserDataByToken(token).data, true);
		
    }
	else if(item.innerHTML == "<h3>browse</h3>"){
		document.getElementById("homepanel").style.display = "none";
        document.getElementById("browsepanel").style.display = "block";		
		document.getElementById("accountpanel").style.display = "none";		
    } 
	else {
		document.getElementById("homepanel").style.display = "none";
		document.getElementById("browsepanel").style.display = "none";
		document.getElementById("accountpanel").style.display = "block";
	}
}

//Welcome page	
var store = function(formData){ 	
	var minpwlength=5;
		
	if((formData.password.value == "") || (formData.password.value.length < minpwlength)) {
		document.getElementById("signUpError").style.color = "red";
		document.getElementById("signUpError").innerHTML = "Minimum length for password is " + minpwlength;		
		return false;		
	}		
	
	if(formData.password.value != formData.rpassword.value)	{
		document.getElementById("signUpError").style.color = "red";
		document.getElementById("signUpError").innerHTML = "Passwords missmatch";
		return false;
	}
	
	var dataObject = {"email": formData.email.value,
                "password": formData.password.value,
                "firstname": formData.firstname.value,
                "familyname": formData.familyname.value,
                "gender": formData.gender.value,
                "city": formData.city.value,
                "country": formData.country.value
				};
		
		var serverResponse = serverstub.signUp(dataObject);
		
		if(serverResponse.success) {
			document.getElementById("signUpError").style.color = "green";
			//clean up 
			formData.email.value = "";
			formData.firstname.value = "";
			formData.familyname.value = "";
			formData.gender.value = "";
			formData.city.value = "";	
			formData.country.value = "";
			formData.password.value = "";
			formData.rpassword.value = "";
			showErrorMessage("signUpError");
		}
		else {
			document.getElementById("signUpError").style.color = "red";
		}
		document.getElementById("signUpError").innerHTML = serverResponse.message;
		
};
var check = function(formData){
	var serverResponse = serverstub.signIn(formData.email.value, formData.password.value);
	if(serverResponse.success) {
		localStorage.setItem("token", JSON.stringify(serverResponse.data));
		displayView();
	} else {
		document.getElementById("signInError").style.color = "red";
		document.getElementById("signInError").innerHTML = serverResponse.message;
	} 
};


/*		To fix:
	Textarea not good enough for wall
*/

/*		Fixxed:
	Field types and required fix.
	Replaced  window alert messages with errortext
	Token using localStorage
	See which user who sent a message
	Change password now repeated field for new password
	
*/
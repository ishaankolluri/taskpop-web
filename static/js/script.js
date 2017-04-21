$(document).ready(function(){
  $('body').removeClass('fade-out');
});

<<<<<<< HEAD

AWSCognito.config.region = 'us-east-1';
var poolData = {
    UserPoolId : 'us-east-1_64kGzQqcZ',
    ClientId : '6ivt62oqie3db5nt68qpoc09uf'
};
var userPool = new AWSCognito.CognitoIdentityServiceProvider.CognitoUserPool(poolData);
//var userPool = new AWSCognito.CognitoUserPool(poolData);


// Send information to AWS Cognito upon sign-in.
=======
>>>>>>> 69387b42ee5468ed19e2320f78c00e585a9a5d2e
function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
<<<<<<< HEAD

  var dataEmail = {
        Name : profile.getName(),
        Value : profile.getEmail()
  };
  var attributeList = [];
  var attributeEmail = new AWSCognito.CognitoIdentityServiceProvider.CognitoUserAttribute(dataEmail);
  attributeList.push(attributeEmail);


  // If this works. pass to AWS cognito, and if authenticated:
  // pull information from dynamo
  // ajax call with JSON to 'home/'
}
=======
  var id_token = googleUser.getAuthResponse().id_token;
  console.log("Send to AWS: " + id_token);
  var json_data = {
    "token": id_token,
    "name": profile.getName(),
    "email": profile.getEmail(),
    "img": profile.getImageUrl()
  }
  // If this works. pass to AWS cognito, and if authenticated:
  // pull information from dynamo
  // ajax call with JSON to 'home/'
  console.log("Attempting to call the home URL");
  $.ajax({
      type: "POST",
      url: "/home/",
      data: json_data,
      failure: function(data){
        console.log("Error: " + data);
      }
    });
}
//
//
// function signOut() {
//     var auth2 = gapi.auth2.getAuthInstance();
//     auth2.signOut().then(function () {
//       console.log('User signed out.');
//     });
//   }
>>>>>>> 69387b42ee5468ed19e2320f78c00e585a9a5d2e

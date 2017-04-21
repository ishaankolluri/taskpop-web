$(document).ready(function(){
  $('body').removeClass('fade-out');
});


AWSCognito.config.region = 'us-east-1';
var poolData = {
    UserPoolId : 'us-east-1_KZ3VOLM6U',
    ClientId : '560pmh9r8gmjrp04aijmnf1tmu'
};
var userPool = new AWSCognito.CognitoIdentityServiceProvider.CognitoUserPool(poolData);
//var userPool = new AWSCognito.CognitoUserPool(poolData);


// Send information to AWS Cognito upon sign-in.
function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
  console.log(googleUser.getAuthResponse().id_token);
  console.log(googleUser.getAuthResponse().id_token.length);

    // TODO: Check if the user is signed in already.
    // TODO: If not, then do the below signup process. Then send them to 'home'.
    // TODO: If they are, redirect them to home with their user information.


  var dataEmail = {
        Name : 'email',
        Value : profile.getEmail()
  };

  var dataName = {
        Name: 'name',
        Value: profile.getName()
  };


  var attributeList = [];
  var attributeEmail = new AWSCognito.CognitoIdentityServiceProvider.CognitoUserAttribute(dataEmail);
  var attributeName = new AWSCognito.CognitoIdentityServiceProvider.CognitoUserAttribute(dataName);
  attributeList.push(attributeName);
  attributeList.push(attributeEmail);
  userPool.signUp(profile.getEmail(), profile.getId(), attributeList, null, function(err, result){
        if (err) {
            alert(err);
            return;
        }
        cognitoUser = result.user;
        console.log('user name is ' + cognitoUser.getUsername());
        $.ajax({
          type: "GET",
          url: "/home/",
          failure: function(data){
            console.log("Error: " + data);
      }
    });
        // If successful, make call to home page.
    });

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

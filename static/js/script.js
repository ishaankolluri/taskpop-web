$(document).ready(function(){
  $('body').removeClass('fade-out');
});


AWSCognito.config.region = 'us-east-1';
var poolData = {
    UserPoolId : 'us-east-1_KZ3VOLM6U',
    ClientId : '560pmh9r8gmjrp04aijmnf1tmu'
};

var userPool = new AWSCognito.CognitoIdentityServiceProvider.CognitoUserPool(poolData);


function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
  console.log(googleUser.getAuthResponse().id_token);
  console.log(googleUser.getAuthResponse().id_token.length);
  var dataName = {
        Name: 'name',
        Value: profile.getName()
  };
  var dataEmail = {
        Name : 'email',
        Value : profile.getEmail()
  };
  var attributeList = [];
  var attributeEmail = new AWSCognito.CognitoIdentityServiceProvider.CognitoUserAttribute(dataEmail);
  var attributeName = new AWSCognito.CognitoIdentityServiceProvider.CognitoUserAttribute(dataName);
  attributeList.push(attributeName);
  attributeList.push(attributeEmail);
  loggedIn(profile, attributeList);
}

function loggedIn(profile, attributeList){
    authentication_data = {
        Username: profile.getEmail(),
        Password: profile.getId()
    };
    var authenticationDetails = new AWSCognito.CognitoIdentityServiceProvider.AuthenticationDetails(authenticationData);
    var userData = {
        Username: profile.getEmail(),
        Pool: userPool
    };
    var cognitoUser = new AWSCognito.CognitoIdentityServiceProvider.CognitoUser(userData);
    cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: function(result){
            // Send access token and username to the 'loggedIn' endpoint
            var access_token = result.getAccessToken.getJwtToken();
            var id_token = result.idToken.jwtToken;
            console.log("Logged In: " + cognitoUser.getUsername());
            // TODO: use Username and access_token to get to home page.
        },
        onFailure: function(err){
            userPool.signUp(profile.getEmail(), profile.getId(), attributeList, null, function(err, result){
                if (err) {
                    alert("Could not sign up: " + err);
                    return;
                }
//                cognitoUser = result.user;
                console.log('Signed up: ' + cognitoUser.getUsername());
                // TODO: Use username to get to home page.
            });
        },
    });
}

// function signOut() {
//     var auth2 = gapi.auth2.getAuthInstance();
//     auth2.signOut().then(function () {
//       console.log('User signed out.');
//     });
//   }

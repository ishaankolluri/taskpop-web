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
  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
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
    var authenticationDetails = new AWSCognito.CognitoIdentityServiceProvider.AuthenticationDetails(authentication_data);
    var userData = {
        Username: profile.getEmail(),
        Pool: userPool
    };
    var cognitoUser = new AWSCognito.CognitoIdentityServiceProvider.CognitoUser(userData);
    console.log("Attempting to authenticate the user.");
    cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: function(result){
            // Send access token and username to the 'loggedIn' endpoint
            var access_token = result.getAccessToken().getJwtToken();
            var id_token = result.idToken.jwtToken;
            console.log("Logged In: " + cognitoUser.getUsername());
            $.ajax({
              type: "POST",
              url: "/session/",
              data: { username: cognitoUser.getUsername() },
              success: console.log('session updated'),
              failure: function(data){
                console.log("Did not update session: " + data);
              }
            });
            window.location.assign('home');
        },
        onFailure: function(err){
            console.log("Registering the user to Cognito for the first time.");
            userPool.signUp(profile.getEmail(), profile.getId(), attributeList, null, function(err, result){
                if (err) {
                    alert("Could not sign up: " + err);
                    return;
                }
                console.log('Successfully signed up: ' + cognitoUser.getUsername());
                $.ajax({
                  type: "POST",
                  url: "/session/",
                  data: { username: cognitoUser.getUsername() },
                  failure: function(data){
                    console.log("Did not update session: " + data);
                  }
                });
                console.log("Put the user in Dynamo for the first time.");
                $.ajax({
                  type: "POST",
                  url: "/firsttimeuser/",
                  data: { username: cognitoUser.getUsername() },
                  failure: function(data){
                    console.log("Did not update username: " + data);
                  }
                });
                window.location.assign('home');
            });
        }
    });
}

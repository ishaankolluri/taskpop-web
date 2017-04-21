$(document).ready(function(){
  $('body').removeClass('fade-out');
});


AWSCognito.config.region = 'us-east-1';
var poolData = {
    UserPoolId : 'us-east-1_64kGzQqcZ',
    ClientId : '6ivt62oqie3db5nt68qpoc09uf'
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

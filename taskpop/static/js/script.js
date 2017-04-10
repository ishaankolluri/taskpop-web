$(document).ready(function(){
  $('body').removeClass('fade-out');
});

function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.

  // If this works. pass to AWS cognito, and if authenticated:
  // pull information from dynamo
  // ajax call with JSON to 'home/'
}

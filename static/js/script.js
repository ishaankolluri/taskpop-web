$(document).ready(function(){
  $('body').removeClass('fade-out');
});

function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
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

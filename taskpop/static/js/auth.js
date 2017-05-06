var data = {
    UserPoolId : 'us-east-1_KZ3VOLM6U',
    ClientId : '560pmh9r8gmjrp04aijmnf1tmu'
};
var userPool = new AWSCognito.CognitoIdentityServiceProvider.CognitoUserPool(data);
var cognitoUser = userPool.getCurrentUser();

if (cognitoUser != null) {
    cognitoUser.getSession(function(err, session) {
        if (err) {
            // There is no session right now.
            $.ajax({
                type: "POST",
                url: "/deauth/",
                failure: function(data){
                    console.log("Did not delete session var.");
                }
            });
            return;
        }
        $.ajax({
          type: "POST",
          url: "/session/",
          data: { username: cognitoUser.getUsername() },
          failure: function(data){
            console.log("Did not update session: " + data);
          }
        });
        console.log('session validity: ' + session.isValid());
        console.log(cognitoUser.getUsername());
    });
}
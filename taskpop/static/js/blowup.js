$(function(){
    $('#save').click(function(event){
        event.preventDefault();
        saveModals();
    });
});

function saveModals(){
    var modals = document.getElementsByClassName("modalContent");
    var i;
    for(i = 0; i < modals.length; i++){
        var inputs = modals[i].getElementsByTagName("input");
        var json_data = {};
        for(var j = 0; j < inputs.length; j++){
            var name = inputs[i].name;
            json_data[name] = inputs[i].value;
        }

        // Hopefully this won't kick in a redirect b/c AJAX.
        $.ajax({
            type: "POST",
            url: "/save/",
            data: {task: JSON.stringify(json_data) },
            success: console.log("Blowup Task Saved."),
            failure: alert("Something went wrong saving.")
        });
    }
    if(i === modals.length - 1){ // Pseudo callback
        var rows = document.getElementsByClassName("tableInfo");
        var ids = [];
        for(var k = 0; k < rows.length; k++){
            ids.push(rows[j].id);
        }
        console.log("Sending reprioritized IDs...");
        $.ajax({
           type: "POST",
            url: "/reprioritize/",
            data: {task_ids: JSON.stringify(ids)},
            success: window.location.assign("edit"),
            failure: function(err){
                alert("Refresh and try again: " + err);
            }
        });
    }
}
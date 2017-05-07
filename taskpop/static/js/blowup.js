$(function(){
    $('#save').click(function(event){
        event.preventDefault();
        saveModals();
    });
});

function saveModals(){
    var rows = document.getElementsByClassName("tableInfo");
    console.log(rows);
        var ids = [];
        for(var k = 0; k < rows.length; k++){
            ids.push(rows[k].id);
        }
        console.log("Sending reprioritized IDs...: " + ids);
        $.ajax({
           type: "POST",
            url: "/reprioritize/",
            data: {task_ids: JSON.stringify(ids)},
            success: function(){
                var host = window.location.hostname;
                window.location.replace("edit");
            },
            failure: function(err){
                alert("Refresh and try again: " + err);
            }
        });
}
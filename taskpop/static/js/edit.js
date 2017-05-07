$(function(){
    $("#reprioritize").click(function(event){
       event.preventDefault();
        var rows = document.getElementsByClassName("tableInfo");
        var ids = [];
        for(var i = 0; i < rows.length; i++){
            ids.push(rows[i].id);
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
    });
});
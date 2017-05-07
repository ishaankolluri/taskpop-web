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

        });

    });

   // $("#{{ task.task_id }}").click(function(event){
   //    event.preventDefault();
   //    var modal = document.getElementById("{{ task.task_id }}_modal");
   //    modal.style.display = "block";
   //    $("#{{ task.task_id }}_close").click(function(event){
   //       modal.style.display = "none";
   //    });
   // });
});
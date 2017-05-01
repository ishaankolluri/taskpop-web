$(function(){
    $("#trashSelected").click(function(event){
        event.preventDefault();
        console.log("Alert!");
        var task_list = [];
        var inputs = document.getElementsByName("trashInput");
        for(var i = 0; i < inputs.length; i++){
            if(inputs[i].checked){
                task_list.push(inputs[i].value);
            }
        }
        if(task_list.length == 0) {
            alert("No task has been selected for deletion.");
        }else{
            $.ajax({
                  type: "POST",
                  url: "/delete/",
                  data: { json_data: JSON.stringify({ tasks: task_list }) },
                  success: window.location.assign('edit'),
                  failure: function(data){
                    console.log("Error deleting: " + data);
                  }
            });
        }
    });
});

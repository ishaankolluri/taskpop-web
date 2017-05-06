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
    $(".drag").sortable();

//    var dragSrcEl = null;
//    function handleDragStart(e){
//        this.style.opacity = 0.4;
//        dragSrcEl = this;
//        e.dataTransfer.effectAllowed = 'move';
//        e.dataTransfer.setData('id, 'this.id);
//    }
//
//    function handleDragOver(e) {
//      if (e.preventDefault) {
//        e.preventDefault(); // Necessary. Allows us to drop.
//      }
//      e.dataTransfer.dropEffect = 'move';  // See the section on the DataTransfer object.
//      return false;
//    }
//    function handleDragEnter(e) {
//      // this / e.target is the current hover target.
//      this.classList.add('over');
//    }
//
//    function handleDragLeave(e) {
//      this.classList.remove('over');  // this / e.target is previous target element.
//    }
//
//    function handleDrop(e) {
//      // this / e.target is current target element.
//
//      if (e.stopPropagation) {
//        e.stopPropagation(); // stops the browser from redirecting.
//      }
//
//      if (dragSrcEl != this) {
//        // Set the source column's HTML to the HTML of the column we dropped on.
//        dragsrcEl.id = this.id;
//        this.id = e.dataTransfer.getData('id');
//        // TODO: Get all the row ids and query reprioritize with list.
//        var ids_in_order = document.querySelectorAll(".drag");
//        $.ajax({
//          type: "POST",
//          url: "/reprioritize/",
//          data: { json_data: ids },
//          success: window.location.assign('edit'),
//          failure: function(data){
//            console.log("Error reprioritizing: " + data);
//          }
//        });
//      }
//
//      return false;
//    }
//
//    function handleDragEnd(e) {
//      // this/e.target is the source node.
//
//      [].forEach.call(cols, function (col) {
//        col.classList.remove('over');
//      });
//    }
//
//    var cols = document.querySelectorAll('.drag');
//    [].forEach.call(cols, function(col) {
//      col.addEventListener('dragstart', handleDragStart, false);
//      col.addEventListener('dragenter', handleDragEnter, false);
//      col.addEventListener('dragover', handleDragOver, false);
//      col.addEventListener('dragleave', handleDragLeave, false);
//      col.addEventListener('drop', handleDrop, false);
//      col.addEventListener('dragend', handleDragEnd, false);
//
//    });
});


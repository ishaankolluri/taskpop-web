$(function(){
   $("#create").click(function(event){
      event.preventDefault();
      var modal = document.getElementById("createModal");
      modal.style.display = "block";
      $("#close").click(function(event){
         modal.style.display = "none";
      });
   });
});


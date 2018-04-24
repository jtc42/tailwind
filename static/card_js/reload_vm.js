// Function to reload device list
function reloadVM() {
    $.ajax({
      url: "/vmdevs",
      type: "get",
      success: function(response) {
        $("#vmlist").html(response);
      },
      error: function(xhr) {
        //Do Something to handle error
      }
    });
}

// Update all dynamics on load
$(document).ready(function(){
    reloadVM();
});

// Update all dynamics every 30000ms
window.setInterval(function(){
    reloadVM();
}, 30000);
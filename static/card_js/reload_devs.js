// Function to reload device list
function reloadDevs() {
    $.ajax({
      url: "/devs",
      type: "get",
      success: function(response) {
        $("#devlist").html(response);
      },
      error: function(xhr) {
        //Do Something to handle error
      }
    });
}

// Update all dynamics on load
$(document).ready(function(){
    reloadDevs();
});

// Update all dynamics every 5000ms
window.setInterval(function(){
    reloadDevs();
}, 5000);
// Function to reload device list
function reloadDiskinfo() {
    $.ajax({
      url: "/diskinfo",
      type: "get",
      success: function(response) {
        $("#disklist").html(response);
      },
      error: function(xhr) {
        //Do Something to handle error
      }
    });
}

// Update all dynamics on load
$(document).ready(function(){
    reloadDiskinfo();
});

// Update all dynamics every 5000ms
window.setInterval(function(){
    reloadDiskinfo();
}, 30000);
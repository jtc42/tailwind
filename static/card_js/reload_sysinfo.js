// Function to reload device list
function reloadSysinfo() {
    $.ajax({
      url: "/sysinfo",
      type: "get",
      success: function(response) {
        $("#syslist").html(response);
      },
      error: function(xhr) {
        //Do Something to handle error
      }
    });
}

// Update all dynamics on load
$(document).ready(function(){
    reloadSysinfo();
});

// Update all dynamics every 5000ms
window.setInterval(function(){
    reloadSysinfo();
}, 5000);
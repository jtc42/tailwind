// Function to reload device list
function reloadVpn() {
    $.ajax({
      url: "/vpndevs",
      type: "get",
      success: function(response) {
        $("#vpnlist").html(response);
      },
      error: function(xhr) {
        //Do Something to handle error
      }
    });
}

// Update all dynamics on load
$(document).ready(function(){
    reloadVpn();
});

// Update all dynamics every 5000ms
window.setInterval(function(){
    reloadVpn();
}, 5000);
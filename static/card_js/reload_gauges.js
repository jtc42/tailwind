// CREATE GAUGES

// Create CPU gauge
var c_gauge = new JustGage({
    id: "cpu_gauge",
    value: 0,
    min: 0,
    max: 100,
    title: "CPU Load (%)"
});

// Create CPU T gauge
var ct_gauge = new JustGage({
    id: "cpt_gauge",
    value: 0,
    min: 20,
    max: 80,
    title: "CPU Temp (°C)"
});

// Create GPU gauge
var g_gauge = new JustGage({
    id: "gpu_gauge",
    value: 0,
    min: 0,
    max: 100,
    title: "GPU Load (%)"
});

// Create GPU T gauge
var gt_gauge = new JustGage({
    id: "gpt_gauge",
    value: 0,
    min: 20,
    max: 80,
    title: "GPU Temp (°C)"
});

// Create RAM gauge
var r_gauge = new JustGage({
    id: "ram_gauge",
    value: 0,
    min: 0,
    max: 100,
    title: "Memory Load (%)"
});

// Create GPU mem gauge
var gm_gauge = new JustGage({
    id: "gpm_gauge",
    value: 0,
    min: 0,
    max: 100,
    title: "GPU Memory Load (%)"
});


// UPDATE GAUGES

// Reload status and gauges
function reloadStats() {
    var stat_dict = {};
    $.getJSON("/gauges", function(result){
        $.each(result, function(i, field){
            stat_dict[i] = field;
        });
        
        c_gauge.refresh(stat_dict["CPU Total/Load"]);
        ct_gauge.refresh(stat_dict["CPU Package/Temperature"]);
        g_gauge.refresh(stat_dict["GPU Core/Load"]);
        gt_gauge.refresh(stat_dict["GPU Core/Temperature"]);
        r_gauge.refresh(stat_dict["Memory/Load"]);
        gm_gauge.refresh(stat_dict["GPU Memory/Load"]);
    });
}

// Update all dynamics on load
$(document).ready(function(){
    reloadStats()
});

// Update all dynamics every 5000ms
window.setInterval(function(){
    reloadStats()
}, 5000);
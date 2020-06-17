$(document).ready(function () {

    loadAndSetData();
    setInterval(loadAndSetData, 60000);
    setInterval(reloadVisualization, 300000);

    function loadAndSetData() {
        $.getJSON("/api/v1/latest/", function (data) {
            setValues(data["inside"], data["outside"], data["latest_formatted"]);
        });
    }

    function setValues(inside, outside, latest) {
        $("#temp_inside").text(inside.toFixed(1));
        $("#temp_outside").text(outside.toFixed(1));
        $("#latest").text(latest);
    }

    function reloadVisualization() {
        let d = new Date()
        $("#mgviz").attr("src", "/static/latest.png?" + d.getTime())
    }

});
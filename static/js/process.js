$(document).ready(function () {

    const MEASUREMENT_START_DATE = new Date(2020,7,12);

    startUI();
    loadAndSetData();
    setInterval(loadAndSetData, 60000);
    setInterval(setCurrentVisualization, 300000);

    function startUI() {
        $("#datepicker").datepicker({
            showOn: "button",
            buttonText: "Select date",
            minDate: MEASUREMENT_START_DATE,
            maxDate: "-1",
            dateFormat: "yymmdd",
            onSelect: function(dateText) {
                setVisualization(dateText);
            }
        });
        $("#currentgraph").on("click", function() {
            setCurrentVisualization();
        });
    }

    function loadAndSetData() {
        $.getJSON("/api/v1/latest/", function (data) {
            setValues(data["inside"], data["outside"], data["latest_formatted"]);
            setOWMData(data["owm_temp"], data["owm_feels"], data["owm_condition"]);
        });
    }

    function setValues(inside, outside, latest) {
        $("#temp_inside").text(inside.toFixed(1));
        $("#temp_outside").text(outside.toFixed(1));
        $("#latest").text(latest);
    }

    function setOWMData(temp, feels, condition) {
        if (parseFloat(temp) < -200.0)
            $("#owm_info").text("No Data");
        else {
            let to_show = "Current " + temp.toFixed(1) + "°C, feels like " + feels.toFixed(1) + "°C, " + condition;
            $("#owm_info").text(to_show);
        }
    }

    function setCurrentVisualization() {
        setVisualization("latest");
    }

    function setVisualization(date_string) {
        let d = new Date();
        $("#mgviz").attr("src", "/static/graphs/" + date_string + ".png?" + d.getTime());
    }

});
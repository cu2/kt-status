$(function() {
  const t = new Date().getTime();
  $.getJSON("/data/current.json?t="+t, function(data) {
    $("#current_response_time").html(Math.round(data.response_time * 1000));
    if (data.success) {
      $("#current_status").css({ color: "green" });
    } else {
      $("#current_status").css({ color: "red" });
    }
  });
  $.getJSON("/data/hours.json?t="+t, function(data) {
    const p95 = data.map(function(item) {
      return Math.round(item.p95 * 1000);
    });
    $("#sparkline_24_hours").sparkline(p95, {
      width: 240,
      height: 30,
      spotColor: "",
      minSpotColor: "",
      maxSpotColor: "",
    });
  });
  $.getJSON("/data/days.json?t="+t, function(data) {
    const p95 = data.map(function(item) {
      return Math.round(item.p95 * 1000);
    });
    $("#sparkline_91_days").sparkline(p95, {
      width: 240,
      height: 30,
      spotColor: "",
      minSpotColor: "",
      maxSpotColor: "",
    });
  });
});

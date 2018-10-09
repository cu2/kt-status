const getResponseTimeSeriesData = function(data, name) {
  return data.map(function(item) {
    return [
      new Date(item.timestamp).getTime(),
      Math.round(item[name] * 1000),
    ];
  });
};

const getSuccessRateSeriesData = function(data) {
  return data.map(function(item) {
    return [
      new Date(item.timestamp).getTime(),
      Math.round(item.success_rate),
    ];
  });
};

const getResponseTimeSeriesConfig = function(data) {
  return ["p95", "p90", "p50", "avg"].map(function(name) {
    return {
      name: name,
      data: getResponseTimeSeriesData(data, name),
      tooltip: {
        valueSuffix: "ms",
      },
    };
  });
};

const getSuccessRateSeriesConfig = function(data) {
  return [{
    name: "Success rate",
    data: getSuccessRateSeriesData(data),
    tooltip: {
      valueSuffix: "%",
    },
  }];
};

const getChartConfig = function(title, series) {
  return {
    chart: {
      type: "line",
      height: 300,
    },
    credits: false,
    time: {
      useUTC: false,
    },
    legend: {
      enabled: false,
    },
    title: {
      text: title,
    },
    tooltip: {
      crosshairs: [true, true]
    },
    xAxis: {
      type: "datetime",
    },
    yAxis: {
      min: 0,
      title: {
        text: null,
      },
    },
    series: series,
  };
};

const createChart = function(renderTo, title, seriesConfig) {
  Highcharts.chart(
    renderTo,
    getChartConfig(
      title,
      seriesConfig,
    ),
  );
};

const pad2 = function(value) {
  if (value < 10) {
    return "0" + value;
  }
  return "" + value;
};

const getDate = function(ts) {
  const d = new Date(ts);
  return [
    d.getFullYear(),
    "-",
    pad2(d.getMonth() + 1),
    "-",
    pad2(d.getDate()),
  ].join("");
};

const getDateHour = function(ts) {
  const d = new Date(ts);
  return [
    getDate(ts),
    " ",
    pad2(d.getHours()),
    ":00:00",
  ].join("");
};

const getDateHMS = function(ts) {
  const d = new Date(ts);
  return [
    getDate(ts),
    " ",
    pad2(d.getHours()),
    ":",
    pad2(d.getMinutes()),
    ":00",
  ].join("");
};

$(function() {
  const t = new Date().getTime();
  $.getJSON("/data/current.json?t="+t, function(data) {
    $("#current_response_time").html(Math.round(data.response_time * 1000));
    $("#current_status").html(data.success ? "Ok" : "Error");
    $("#current_datetime").html(getDateHMS(data.timestamp));
  });
  $.getJSON("/data/hours.json?t="+t, function(data) {
    createChart(
      "response_time_chart_24_hours",
      "Response times in last 24 hours",
      getResponseTimeSeriesConfig(data),
    );
    createChart(
      "success_rate_chart_24_hours",
      "Success rates in last 24 hours",
      getSuccessRateSeriesConfig(data),
    );
    const lastHour = data[data.length - 1];
    $("#last_hour_response_time_p95").html(Math.round(lastHour.p95 * 1000));
    $("#last_hour_response_time_p90").html(Math.round(lastHour.p90 * 1000));
    $("#last_hour_response_time_p50").html(Math.round(lastHour.p50 * 1000));
    $("#last_hour_response_time_avg").html(Math.round(lastHour.avg * 1000));
    $("#last_hour_success_rate").html(lastHour.success_rate);
    $("#last_hour_datetime").html(getDateHour(lastHour.timestamp));
  });
  $.getJSON("/data/days.json?t="+t, function(data) {
    createChart(
      "response_time_chart_91_days",
      "Response times in last 91 days",
      getResponseTimeSeriesConfig(data),
    );
    createChart(
      "success_rate_chart_91_days",
      "Success rates in last 91 days",
      getSuccessRateSeriesConfig(data),
    );
    const lastDay = data[data.length - 1];
    $("#last_day_response_time_p95").html(Math.round(lastDay.p95 * 1000));
    $("#last_day_response_time_p90").html(Math.round(lastDay.p90 * 1000));
    $("#last_day_response_time_p50").html(Math.round(lastDay.p50 * 1000));
    $("#last_day_response_time_avg").html(Math.round(lastDay.avg * 1000));
    $("#last_day_success_rate").html(lastDay.success_rate);
    $("#last_day_datetime").html(getDate(lastDay.timestamp));
  });
});

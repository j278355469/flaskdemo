const Chart1 = echarts.init(document.getElementById('main'));
const Chart2 = echarts.init(document.getElementById('six-county'));
const Chart3 = echarts.init(document.getElementById('county'));
const selectCountyE1 = document.querySelector("#selectCounty")

selectCountyE1.addEventListener("change", () => {
    console.log(selectCountyE1.value);
    drawCountyPM25(selectCountyE1.value)


});
window.onresize = function () {
    chart1.resize();
    chart2.resize();
    chart3.resize();
}



drawPM25();



function chartpic(chart, title, label, xData, yData, color = "") {
    let option = {
        title: {
            text: title
        },
        tooltip: {},
        legend: {
            data: ['label']
        },
        xAxis: {
            data: xData
        },
        yAxis: {},
        series: [
            {
                itemStyle: {
                    color: color
                },

                name: 'label',
                type: 'bar',
                data: yData
            }
        ]
    };

    chart.setOption(option);
}

function drawCountyPM25(county) {
    Chart3.showLoading();

    $.ajax(
        {
            url: "/county-pm25-json/" + county,
            type: "GET",
            dataType: "json",
            success: (result) => {
                Chart3.hideLoading();
                console.log(result);
                chartpic(Chart3, county, 'PM2.5',
                    Object.keys(result['pm25']),
                    Object.values(result['pm25']),
                    color = "d2ed6d",
                )
            },

            error: () => {
                Chart3.hideLoading();
                alert("取得資料失敗!");
            }
        }
    )
}



// function echartSixPm25(result) {
//     let option = {
//         title: {
//             text: '六都PM2.5平均值'
//         },
//         tooltip: {},
//         legend: {
//             data: ['PM2.5']
//         },
//         xAxis: {
//             data: Object.keys(result)
//         },
//         yAxis: {},
//         series: [
//             {
//                 name: 'PM2.5',
//                 type: 'bar',
//                 data: Object.values(result)
//             }
//         ]
//     };

//     Chart2.setOption(option);
// }

// function echartPic1(result) {
//     let option = {
//         title: {
//             text: result["title"]
//         },
//         tooltip: {},
//         legend: {
//             data: ['PM2.5']
//         },
//         xAxis: {
//             data: result['xData']
//         },
//         yAxis: {},
//         series: [
//             {
//                 name: 'PM2.5',
//                 type: 'bar',
//                 data: result['yData']
//             }
//         ]
//     };

//     Chart1.setOption(option);
// }



function drawPM25() {
    Chart1.showLoading();
    Chart2.showLoading();
    $.ajax(
        {
            url: "/pm25-json",
            type: "GET",
            dataType: "json",
            success: (result) => {
                Chart1.hideLoading();
                Chart2.hideLoading();
                console.log(result);

                chartpic(Chart1, result["title"], 'PM2.5',
                    result['xData'],
                    result['yData'])



                chartpic(Chart2, '六都PM2.5平均值', 'PM2.5',
                    Object.keys(result['sixData']),
                    Object.values(result['sixData']),)

                drawCountyPM25(result["county"]);
            },
            error: () => {
                Chart1.hideLoading();
                Chart2.hideLoading();
                alert("取得資料失敗!");
            }
        }
    )
}

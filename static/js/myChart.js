function lineChart(myChart, title, route, yLabel){

    d3.json(route).then(function(data) {
        // won't display due to missing y-values
        x = data.unit
        y = data.absenses 

        // var trace2 = {
        //     x: [2, 3, 4, 5],
        //     y: [],
        //     mode: 'lines',
        //     line: {
        //         color: 'rgb(55, 128, 191)',
        //         width: 3
        //     }
        // };

        var trace3 = {
            x: x,
            y: y,
            mode: 'lines+markers',
            marker: {
                color: '#0B5394',
                size: 6
            },
            line: {
                color: '#0B5394',
                width: 3
            },
            name: "Absenses"
        };

        var data = [trace3];

        var layout = {
            // title: {
            //     text: title,
            //     font: {
            //         color:"#000",
            //         family: "Arial",
            //         size:30

            //     },
            //     pad: {
            //         b:0,
            //         l:0,
            //         r:0,
            //         t:0
            //     },
            //     xanchor:"auto",
            //     yanchor:"top",
            //     x:0.5,
            //     y:0.85
            // },
            xaxis: {
                title: 'Week',
                showgrid: false,
                zeroline: false
            },
            yaxis: {
                title: yLabel,
                showline: false
            },
            plot_bgcolor: "#F1F2F4",
            paper_bgcolor:  "#fff",
            margin: {
                    l: 50,
                    r: 50,
                    b: 50,
                    t: 50,
                    pad: 4
            }
        };

        var config = {responsive: true}

        Plotly.newPlot(myChart, data, layout, config);
    })
}

function feedbackLineChart(myChart, title, route, yLabel){

    d3.json(route).then(function(data) {
        x = data.week
        y1 = data.satisfaction 
        y2 = data.support
        y3 = data.outside_learning 
        y4 = data.pace 
        y5 = data.engagement
        y6 = data.clarity 
        y7 = data.knowledge 
        y8 = data.homework 
        y9 = data.time 
        
        var trace1 = {
            x: x,
            y: y1,
            mode: 'lines+markers',
            marker: {
                color: '#e3342f',
                size: 6
            },
            line: {
                color: '#e3342f',
                width: 3
            },
            name:  'Overall Satisfaction'
        };

        var trace2 = {
            x: x,
            y: y2,
            mode: 'lines+markers',
            marker: {
                color: '#f6993f',
                size: 6
            },
            line: {
                color: '#f6993f',
                width: 3
            },
            name: 'Academic Support'
        };

        var trace3 = {
            x: x,
            y: y3,
            mode: 'lines+markers',
            marker: {
                color: '#ffed4a',
                size: 6
            },
            line: {
                color: '#ffed4a',
                width: 3
            },
            name: 'Outside Productivity'
        };

        var trace4 = {
            x: x,
            y: y4,
            mode: 'lines+markers',
            marker: {
                color: '#38c172',
                size: 6
            },
            line: {
                color: '#38c172',
                width: 3
            },
            name: 'Pace'
        };

        var trace5 = {
            x: x,
            y: y5,
            mode: 'lines+markers',
            marker: {
                color: '#4dc0b5',
                size: 6
            },
            line: {
                color: '#4dc0b5',
                width: 3
            },
            name:  'Engagement'
        };

        var trace6 = {
            x: x,
            y: y6,
            mode: 'lines+markers',
            marker: {
                color: '#3490dc',
                size: 6
            },
            line: {
                color: '#3490dc',
                width: 3
            },
            name: 'Instructor Clarity'
        };

        var trace7 = {
            x: x,
            y: y7,
            mode: 'lines+markers',
            marker: {
                color: '#6574cd',
                size: 6
            },
            line: {
                color: '#6574cd',
                width: 3
            },
            name: 'Instructor Knowledge'
        };

        var trace8 = {
            x: x,
            y: y8,
            mode: 'lines+markers',
            marker: {
                color: '#9561e2',
                size: 6
            },
            line: {
                color: '#9561e2',
                width: 3
            },
            name: 'Homework Feedback'
        };

        var trace9 = {
            x: x,
            y: y9,
            mode: 'lines+markers',
            marker: {
                color: '#f66d9b',
                size: 6
            },
            line: {
                color: '#f66d9b',
                width: 3
            },
            name:'Time Spent Outside Class'
        };

        var datum = [trace1, trace2, trace3, trace4, 
            trace5, trace6, trace7, trace8, trace9];

        var layout = {
            // title: {
            //     text: title,
            //     font: {
            //         color:"#000",
            //         family: "Arial",
            //         size:30

            //     },
            //     pad: {
            //         b:0,
            //         l:0,
            //         r:0,
            //         t:0
            //     },
            //     xanchor:"auto",
            //     yanchor:"top",
            //     x:0.5,
            //     y:0.85
            // },
            xaxis: {
                title: 'Week',
                showgrid: false,
                zeroline: false
            },
            yaxis: {
                title: yLabel,
                showline: false
            },
            plot_bgcolor: "#F1F2F4",
            paper_bgcolor:  "#fff",
            margin: {
                    l: 50,
                    r: 50,
                    b: 50,
                    t: 50,
                    pad: 4
            }
        };

        var config = {responsive: true}

        Plotly.newPlot(myChart, datum, layout, config);
    })
}


function negativeBarChart(myChart, title, x, y, yLabel){

    var trace = {
        x: x,
        y: y,
        name: 'given name',
        type: 'bar'
    };

    var data = [trace];
    var layout = { 
        // title: {
        //     text: title,
        //     pad: {
        //         b:0,
        //         l:0,
        //         r:0,
        //         t:0
        //     },
        //     xanchor:"auto",
        //     yanchor:"auto"
        // },
        xaxis: {
            title: 'Week Number',
            showgrid: false,
            zeroline: false
        },
        yaxis: {
            title: yLabel,
            showline: false
        },
        plot_bgcolor: "#F1F2F4",
        paper_bgcolor:  "#fff",
        margin: {
            l: 50,
            r: 50,
            b: 50,
            t: 50,
            pad: 4
        }
    };


    var config = {
    modeBarButtons: [[{
        name: 'stack',
        click: function(gd) {
        Plotly.relayout(gd, 'barmode', 'stack');
        }
    }, {
        name: 'overlay',
        click: function(gd) {
        Plotly.relayout(gd, 'barmode', 'overlay');
        }
    }, {
        name: 'group',
        click: function(gd) {
        Plotly.relayout(gd, 'barmode', 'group');
        }, 
    }, {
        name: 'relative',
        click: function(gd) {
        Plotly.relayout(gd, 'barmode', 'relative');
        }, 
    }].reverse()],

    responsive: true
    }

    Plotly.newPlot(myChart, data, layout, config);

}

function submissionsBarChart(myChart, title, route, yLabel){
    // x, y1, y2, y3, y4
    d3.json(route).then(function(data) {
        let x = data.unit 
        let y1 = data.veryearly
        let y2 = data.early 
        let y3 = data.ontime
        let y4 = data.late 
        let y5 = data.verylate
        let y6 = data.notsubmitted

        var trace1 = {
            x: x,
            y: y1,
            name: 'Very Early',
            type: 'bar',
            marker: {
                color: "#073b4c"
            }
        };

        var trace2 = {
            x: x,
            y: y2,
            name: 'Early',
            type: 'bar',
            marker: {
                color: "#118ab2"
            }
        };

        var trace3 = {
            x: x,
            y: y3,
            name: 'On-Time',
            type: 'bar',
            marker: {
                color: "#06d6a0"
            }
        };

        var trace4 = {
            x: x,
            y: y4,
            name: 'Late',
            type: 'bar',
            marker: {
                color: "#ffd166"
            }
        };

        var trace5 = {
            x: x,
            y: y5,
            name: 'Very Late',
            type: 'bar',
            marker: {
                color: "#F76915"
            }
        };

        var trace6 = {
            x: x,
            y: y6,
            name: 'Not Submitted',
            type: 'bar',
            marker: {
                color: "#fd0100"
            }
        };

        var traces = [trace1, trace2, trace3, trace4, trace5, trace6];
        var layout = { 
            // title: {
            //     text: title,
            //     pad: {
            //         b:0,
            //         l:0,
            //         r:0,
            //         t:0
            //     },
            //     xanchor:"auto",
            //     yanchor:"auto"
            // },
            xaxis: {
                title: 'Unit #',
                showgrid: false,
                zeroline: false
            },
            yaxis: {
                title: yLabel,
                showline: false
            },
            plot_bgcolor: "#F1F2F4",
            paper_bgcolor:  "#fff",
            margin: {
                l: 50,
                r: 50,
                b: 50,
                t: 50,
                pad: 4
            }
        };

        var config = {responsive: true}

    Plotly.newPlot(myChart, traces, layout, config)
    })
}


function stdList(route, id, text){

    d3.json(route).then(function(data) {
        let ul_element = d3.select('#'+id)
        data.forEach(element => {
            ul_element.append("li")
                      .classed("list-group-item", true)
                      .text(element[0]+ " - " + text + " " + element[1])
        });
        

    })
};

function stdTable(route, id){

    d3.json(route).then(function(data){
        let tbody_element = d3.select('#'+id)
        data.forEach(element => {
            let rows = tbody_element.selectAll("tr")
                        .data(data)
                        .enter()
                        .append("tr")
            let cells = rows.selectAll('td')
                        .data(function (d) { return d })
                        .enter()
                        .append('td')
                        .text(function (d) { return d });

        })
    })
};

function cohortDropdown(route, id){
    d3.json(route).then(function(data){
        let selector = d3.select('#'+id)
        data.unshift([])
        data.forEach(element => {
            let rows = selector.selectAll("option")
                                .data(data)
                                .enter()
                                .append("option")
                                .attr("value", function(d) {return d[1]})
                                .text(function(d) {return d[0]})
                                .merge(selector);

        })
    });
    // executes after populationg the dropdown
    // sets the default selected item
    cohortDropdownSelection();
};

function cohortDropdownSelection(){
    let selector = d3.select('#cohort-select')
    d3.json('api/currentcohort').then(function(data){
        selector.node().value = data.cohort_number
        // probably not the best way of doing this 
        // but it works for now
    })
};
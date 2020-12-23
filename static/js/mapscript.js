//map showing farms
var H = Highcharts,
    map = H.maps['countries/ug/ug-all'],
    chart;

// Highcharts.getJSON('/farm/api/maps/', function (json) {
//     var data = [];
//     json.forEach(function (p) {
//         p.z = p.land_occupied;
//         data.push(p);
//     })

// // console.log(data)  
//     chart = Highcharts.mapChart('farm_container', {
//         title: {
//             text: 'Farmers Locations'
//         },
        
//         boost:{
//           allowForce:true,
//         },
    
//         mapNavigation: {
//             enabled: true,
//             buttonOptions: {
//                 verticalAlign: 'bottom'
//             }
//         },
       
//         tooltip: {
//             pointFormat:'farm name: {point.farm_name}<br>' +

//                 // 'district: {point.district}<br>' +
//                 'farmer: {point.farmer}<br>' +
//                 'Phone Number: {point.phone_number}<br>' +
//                 'land occupied: {point.land_occupied}'+ ' acres'
      
//         },

//         xAxis: {
//             crosshair: {
//                 zIndex: 5,
//                 dashStyle: 'dot',
//                 snap: false,
//                 color: 'gray'
//             }
//         },

//         yAxis: {
//             crosshair: {
//                 zIndex: 5,
//                 dashStyle: 'dot',
//                 snap: false,
//                 color: 'gray'
//             }
//         },
//         plotOptions:{
//             series:{
//                 point:{
//                     events:{
//                         click: function(event){
//                              var url = "/farm/"+ event.point.id +"/view/";
//                              window.location.href = url;
//                             //alert(event.point.id);
//                         }
//                     }
//                 }
//             }
//         },
//         series: [{
//             boostThreshold: 50, 
//             name: 'Basemap',
//             mapData: map,
//             borderColor: '#B0B0B0',
//             nullColor: 'rgba(200, 200, 200, 0.2)',
//             showInLegend: false
//         }, {
//             name: 'Separators',
//             type: 'mapline',
//             data: H.geojson(map, 'mapline'),
//             color: '#101010',
//             enableMouseTracking: false,
//             showInLegend: false
//         }, {
//             type: 'mapbubble',
//             dataLabels: {
//                 enabled: true,
//                 format: '{point.farm_name}'
//             },
//             name: 'Farms',
//             data: data,
//             maxSize: '5%',
//             color: 'green'
//         }]
//     });
// });


// Display custom label with lat/lon next to crosshairs
document.getElementById('farm_container').addEventListener('mousemove', function (e) {
    var position;
    if (chart) {
        if (!chart.lab) {
            chart.lab = chart.renderer.text('', 0, 0)
                .attr({
                    zIndex: 5
                })
                .css({
                    color: '#505050'
                })
                .add();
        }

        e = chart.pointer.normalize(e);
        position = chart.fromPointToLatLon({
            x: chart.xAxis[0].toValue(e.chartX),
            y: chart.yAxis[0].toValue(e.chartY)
        });
      
        chart.lab.attr({
            x: e.chartX + 5,
            y: e.chartY - 22,
            text: 'Lat: ' + position.lat.toFixed(2) + '<br>Lon: ' + position.lon.toFixed(2)
        });
    }
});


document.getElementById('farm_container').addEventListener('mouseout', function () {
    if (chart && chart.lab) {
        chart.lab.destroy();
        chart.lab = null;
    }
});


//map showing resources
 Highcharts.getJSON('/resourcesharing/api/resource/', function (json) {
  var data = [];
  json.forEach(function (p) {
      p.z = p.id;
      data.push(p);
  })
//console.log(data);
 
  chart = Highcharts.mapChart('resource_container', {
      title: {
          text: 'Resource Locations'
      },
       
      boost:{
        allowForce:true,
      },
  
      mapNavigation: {
          enabled: true,
          buttonOptions: {
              verticalAlign: 'bottom'
          }
      },
     
      tooltip: {
          pointFormat:
          'Owner: {point.owner}<br>' +
          'Resource Status: {point.resource_status}<br>' +
          'Price: {point.price}<br>' + 'shs'
          
      },

      xAxis: {
          crosshair: {
              zIndex: 5,
              dashStyle: 'dot',
              snap: false,
              color: 'gray'
          }
      },

      yAxis: {
          crosshair: {
              zIndex: 5,
              dashStyle: 'dot',
              snap: false,
              color: 'gray'
          }
      },
      plotOptions:{
          series:{
              point:{
                  events:{
                      click: function(event){
                           var url = "/resourcesharing/"+ event.point.id +"/view/";
                           window.location.href = url;
                          //alert(event.point.id);
                      }
                  }
              }
          }
      },
      series: [{
          boostThreshold: 50, 
          name: 'Basemap',
          mapData: map,
          borderColor: '#B0B0B0',
          nullColor: 'rgba(200, 200, 200, 0.2)',
          showInLegend: false
      }, {
          name: 'Separators',
          type: 'mapline',
          data: H.geojson(map, 'mapline'),
          color: '#101010',
          enableMouseTracking: false,
          showInLegend: false
      }, {
          type: 'mapbubble',
          dataLabels: {
              enabled: true,
              format: '{point.resource_name}'
          },
          name: 'Resources',
          data: data,
          maxSize: '5%',
          color: 'blue'
      }]
  });
});


// Display custom label with lat/lon next to crosshairs
document.getElementById('resource_container').addEventListener('mousemove', function (e) {
  var position;
  if (chart) {
      if (!chart.lab) {
          chart.lab = chart.renderer.text('', 0, 0)
              .attr({
                  zIndex: 5
              })
              .css({
                  color: '#505050'
              })
              .add();
      }

      e = chart.pointer.normalize(e);
      position = chart.fromPointToLatLon({
          x: chart.xAxis[0].toValue(e.chartX),
          y: chart.yAxis[0].toValue(e.chartY)
      });
      
      chart.lab.attr({
          x: e.chartX + 5,
          y: e.chartY - 22,
          text: 'Lat: ' + position.lat.toFixed(2) + '<br>Lon: ' + position.lon.toFixed(2)
      });
  }
});


document.getElementById('resource_container').addEventListener('mouseout', function () {
  if (chart && chart.lab) {
      chart.lab.destroy();
      chart.lab = null;
  }
});

//map showing services
Highcharts.getJSON('/openmarket/api/serviceregistration/', function (json) {
  var data = [];
  json.forEach(function (p) {
      p.z = p.id;
      data.push(p);
  })

 
  chart = Highcharts.mapChart('service_container', {
      title: {
          text: 'Service Locations'
      },
      
      mapNavigation: {
          enabled: true,
          buttonOptions: {
              verticalAlign: 'bottom'
          }
      },
     
      tooltip: {
          pointFormat: 'Service Name: {point.service_name}<br>' +
              'Service Type: {point.service_type}<br>' +
              'Availability Date: {point.availability_date}<br>' 
    
      },

      xAxis: {
          crosshair: {
              zIndex: 5,
              dashStyle: 'dot',
              snap: false,
              color: 'gray'
          }
      },

      yAxis: {
          crosshair: {
              zIndex: 5,
              dashStyle: 'dot',
              snap: false,
              color: 'gray'
          }
      },
      plotOptions:{
          series:{
              point:{
                  events:{
                      click: function(event){
                           var url = "/openmarket/"+ event.point.id +"/view/";
                           window.location.href = url;
                          //alert(event.point.id);
                      },
                  }
              }
          }
      },
      series: [{
          name: 'Basemap',
          mapData: map,
          borderColor: '#B0B0B0',
          nullColor: 'rgba(200, 200, 200, 0.2)',
          showInLegend: false
      }, {
          name: 'Separators',
          type: 'mapline',
          data: H.geojson(map, 'mapline'),
          color: '#101010',
          enableMouseTracking: false,
          showInLegend: false
      }, {
          type: 'mapbubble',
          dataLabels: {
              enabled: true,
              format: '{point.service_name}'
          },
          name: 'services',
          data: data,
          maxSize: '5%',
          color: 'red'
      }]
  });
});


// Display custom label with lat/lon next to crosshairs
document.getElementById('service_container').addEventListener('mousemove', function (e) {
  var position;
  if (chart) {
      if (!chart.lab) {
          chart.lab = chart.renderer.text('', 0, 0)
              .attr({
                  zIndex: 5
              })
              .css({
                  color: '#505050'
              })
              .add();
      }

      e = chart.pointer.normalize(e);
      position = chart.fromPointToLatLon({
          x: chart.xAxis[0].toValue(e.chartX),
          y: chart.yAxis[0].toValue(e.chartY)
      });
    
      chart.lab.attr({
          x: e.chartX + 5,
          y: e.chartY - 22,
          text: 'Lat: ' + position.lat.toFixed(2) + '<br>Lon: ' + position.lon.toFixed(2)
      });
  }
});


document.getElementById('service_container').addEventListener('mouseout', function () {
  if (chart && chart.lab) {
      chart.lab.destroy();
      chart.lab = null;
  }
});


// Create the chart
Highcharts.chart('piecontainer', {
  chart: {
    type: 'pie'
  },
  title: {
    text: 'Number of farmers '
  },
  subtitle: {
    text: 'Click the slices to view versions. Source: <a href="http://statcounter.com" target="_blank">statcounter.com</a>'
  },

  accessibility: {
    announceNewData: {
      enabled: true
    },
    point: {
      valueSuffix: '%'
    }
  },

  plotOptions: {
    series: {
      dataLabels: {
        enabled: true,
        format: '{point.name}: {point.y:.1f}%<br>' 
      }
    }
  },

  tooltip: {
    headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
    pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total farmers<br/>'+
                 '<span style="color:{point.color}">{point.sectorone}</span>: <b>{point.one:.2f}%</b> of total sectors<br/>'+
                 '<span style="color:{point.color}">{point.sectortwo}</span>: <b>{point.two:.2f}%</b> of total sectors<br/>'+
                 '<span style="color:{point.color}">{point.sectorthree}</span>: <b>{point.three:.2f}%</b> of total sectors<br/>'+
                 '<span style="color:{point.color}">{point.sectorfour}</span>: <b>{point.four:.2f}%</b> of total sectors<br/>'
  },

  series: [
    {
      name: "Farmers",
      colorByPoint: true,
      data: [
        {
          name: "Western",
          sectorone: "Livestock",
          sectortwo: "Poultry",
          sectorthree: "Fishery",
          sectorfour: "Crops",
          y: 62.74,
          one: 15.68,
          two: 3.92,
          three: 3.92,
          four: 3.92
        },
        {
          name: "Northern",
          sectorone: "Livestock",
          sectortwo: "Poultry",
          sectorthree: "Fishery",
          sectorfour: "Crops",
          y: 10.57,
          one: 15.68,
          two: 3.92,
          three: 3.92,
          four: 3.92
        },
        {
          name: "Central",
          sectorone: "Livestock",
          sectortwo: "Poultry",
          sector3: "Fishery",
          sector4: "Crops",
          y: 7.23,
          one: 15.68,
          two: 3.92,
          three: 3.92,
          four: 3.92
        },
        {
          name: "Eastern",
          sectorone: "Livestock",
          sectortwo: "Poultry",
          sector3: "Fishery",
          sector4: "Crops",
          y: 5.58,
          one: 15.68,
          two: 3.92,
          three: 3.92,
          four: 3.92
        }
      ]
    }
  ]
});
 

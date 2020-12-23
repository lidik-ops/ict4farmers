$(document).ready(function () {
    //alert('It works');
});
(function ($) {
    "use strict";
    $(".mobile-toggle").click(function () {
        $(".nav-menus").toggleClass("open");
    });
    $(".mobile-search").click(function () {
        $(".form-control-plaintext").toggleClass("open");
    });
    $(".form-control-plaintext").keyup(function (e) {
        if (e.target.value) {
            $("body").addClass("offcanvas");
        } else {
            $("body").removeClass("offcanvas");
        }
    });
})(jQuery);

$('.loader-wrapper').fadeOut('slow', function () {
    $(this).remove();
});

$(window).on('scroll', function () {
    if ($(this).scrollTop() > 600) {
        $('.tap-top').fadeIn();
    } else {
        $('.tap-top').fadeOut();
    }
});
$('.tap-top').click(function () {
    $("html, body").animate({
        scrollTop: 0
    }, 600);
    return false;
});

function toggleFullScreen() {
    if ((document.fullScreenElement && document.fullScreenElement !== null) ||
        (!document.mozFullScreen && !document.webkitIsFullScreen)) {
        if (document.documentElement.requestFullScreen) {
            document.documentElement.requestFullScreen();
        } else if (document.documentElement.mozRequestFullScreen) {
            document.documentElement.mozRequestFullScreen();
        } else if (document.documentElement.webkitRequestFullScreen) {
            document.documentElement.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);
        }
    } else {
        if (document.cancelFullScreen) {
            document.cancelFullScreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.webkitCancelFullScreen) {
            document.webkitCancelFullScreen();
        }
    }
}
(function ($, window, document, undefined) {
    "use strict";
    var $ripple = $(".js-ripple");
    $ripple.on("click.ui.ripple", function (e) {
        var $this = $(this);
        var $offset = $this.parent().offset();
        var $circle = $this.find(".c-ripple__circle");
        var x = e.pageX - $offset.left;
        var y = e.pageY - $offset.top;
        $circle.css({
            top: y + "px",
            left: x + "px"
        });
        $this.addClass("is-active");
    });
    $ripple.on(
        "animationend webkitAnimationEnd oanimationend MSAnimationEnd",
        function (e) {
            $(this).removeClass("is-active");
        });
})(jQuery, window, document);

$(".chat-menu-icons .toogle-bar").click(function () {
    $(".chat-menu").toggleClass("show");
});


/*=====================
 05. Image to background js
 ==========================*/
$(".bg-img").parent().addClass('bg-size');

jQuery('.bg-img').each(function () {

    var el = $(this),
        src = el.attr('src'),
        parent = el.parent();

    parent.css({
        'background-image': 'url(' + src + ')',
        'background-size': 'cover',
        'background-position': 'center',
        'display': 'block'
    });

    el.hide();
});

// Avatar Switcher
function avatarSwitcher() {
    var readURL = function (input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('.profile-pic').attr('src', e.target.result);
            };

            reader.readAsDataURL(input.files[0]);
        }
    };

    $(".file-upload").on('change', function () {
        readURL(this);
    });

    $(".upload-button").on('click', function () {
        $(".file-upload").click();
    });
}

avatarSwitcher();




/// open weather api//
$(document).ready(function () {
    var options = {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 0
    };
    
    function success(pos) {
      var crd = pos.coords;
      var wheather_api = "https://api.openweathermap.org/data/2.5/weather?lat="+crd.latitude+"&lon="+crd.longitude+"&appid=b63fe7d4cf27f561ccaed0342922db91";
      var dairy_weather_url = "https://api.openweathermap.org/data/2.5/onecall?lat="+crd.latitude+"&lon="+crd.longitude+"&exclude=hourly,current,minutely,&appid=b63fe7d4cf27f561ccaed0342922db91";
      var community_weather_url = "/weather/api/community_weather/?lon="+crd.longitude+"&lat="+crd.latitude;
      console.log(community_weather_url);
      // console.log('Your current position is:');
     // console.log(`Latitude : ${crd.latitude}`);
     // console.log(`Longitude: ${crd.longitude}`);
      // console.log(`More or less ${crd.accuracy} meters.`);
      $.ajax({
        url: wheather_api,
        dataType: 'json',
        type:'GET',
        data:{units:'metric'},
        success:function(data){
          
          var weather='';
          $.each(data.weather, function(index,val){
            var icon ="http://openweathermap.org/img/wn/"+val.icon+"@2x.png"
            weather+='<img src='+icon+'><br>'+'<p><h3>'+ data.name+'</b></h3>'+
            data.main.temp +'&deg;C'+'|'+val.main+ ','+
            val.description
  
          });
          $('#showweather').html(weather);
        }
  
      });
      $.ajax({
        url: community_weather_url,
        dataType: 'json',
        type:'GET',
        data:{},
        success:function(data){
         // console.log(data);
          var community_weather='';
          $.each(data, function(index, val){
            var village =val.village.split(",")[0];
            var icon ="http://openweathermap.org/img/wn/"+val.icon+"@2x.png"
            community_weather+='<img src='+icon+'><br>'+'<h3>'+ village +'</b></h3><span>'+
            val.date_reported +'|'+ val.time_reported + ', '+val.weather+'</span>'
  
          });
          $('#show_community_weather').html(community_weather);
        }
  
      });
     
   
    }
    
    function error(err) {
      console.warn(`ERROR(${err.code}): ${err.message}`);
    }
    
    navigator.geolocation.getCurrentPosition(success, error, options);
  
  
    var getFutureDate = function (day) {
      var someDate = new Date();
      var numberOfDaysToAdd = day;
      someDate.setDate(someDate.getDate() + numberOfDaysToAdd); 
    
      var dd = someDate.getDate();
      var mm = someDate.getMonth();
      var y = someDate.getFullYear();
      var d = someDate.getDay();
    
      // convert month number to month name
      var month = new Array();
      month[0] = 'January';
      month[1] = 'February';
      month[2] = 'March';
      month[3] = 'April';
      month[4] = 'May';
      month[5] = 'June';
      month[6] = 'July';
      month[7] = 'August';
      month[8] = 'September';
      month[9] = 'October';
      month[10] = 'November';
      month[11] = 'December';
    
      // convert day number into day name
      var day = new Array();
      day[1] = 'Monday';
      day[2] = 'Tuesday';
      day[3] = 'Wednesday';
      day[4] = 'Thursday'; 
      day[5] = 'Friday';
      day[6] = 'Saturday';
      day[0] = 'Sunday';
    
      var futureMonth = month[mm];
      var futureDay = day[d];
    
      var someFormattedDate = futureDay + ", " + futureMonth + ' '+ dd + ', '+ y;
    
      return someFormattedDate;
    }
    // Function evaluates "clouds" conditions between 1 and 100 and returns image index
    var getClouds = function(clouds) {
      if ( 100 < clouds && clouds < 90 ) {
        // return Cloudy Object
        var condition = {
          cloudNumber: 6,
          cloudText: 'Cloudy'
        };
        return condition;
      } else if ( 89 < clouds && clouds < 60 ) {
        // return Mostly Cloudy
        var condition = {
          cloudNumber: 5,
          cloudText: 'Mostly Cloudy'
        };
        return condition;
      } else if ( 59 < clouds && clouds < 30 ) {
        // return Partly Cloudy
        var condition = {
          cloudNumber: 4,
          cloudText:'Partly Cloudy'
        };
      } else if (29 < clouds && clouds > 20) {
        // return Mostly Sunny
        var condition =  {
          cloudNumber: 3,
          cloudText: 'Mostly Sunny'
        };
        return condition;
      } else if ( 19 > clouds && clouds > 10 ) {
        // return Sunny to Mostly Sunny
        var condition = {
          cloudNumber: 2,
          cloudText: 'Sunny to Mostly Sunny'
        };
        return condition;
      } else {
        // return Sunny
        var condition = {
          cloudNumber: 1,
          cloudText: 'Sunny'
        };
        return condition;
      }
    }
    
    // Function: Handlebar Module / CRPA ("Crapa") (Create, Reference, Pass & Append)
    var getWeather = function(theForecast) {
      // City Label
      $('#results').html(theForecast.city.name);
      // REFERENCE from HTML
      var source = $('#weather-spot').html();
      // compile to Handlebars
      var template = Handlebars.compile(source);
    
      // create loop to get x days worth of data.  "list" is key name.
      for (var i = 1 ; i < theForecast.list.length; i++) {
        // get future dates
        var futureDate = getFutureDate(i);
        var cloudsCondition = getClouds(theForecast.list[i].clouds);
        
        // build weather data object for Handlebars
        var weatherData = {
          now: futureDate,
          average: Math.round(theForecast.list[i].temp.day),
          high: Math.round(theForecast.list[i].temp.max),
          low: Math.round(theForecast.list[i].temp.min),
          morning: Math.round(theForecast.list[i].temp.morn),
          nighttime: Math.round(theForecast.list[i].temp.night),
          cloudInfo: cloudsCondition.cloudNumber,
          cloudInfoText: cloudsCondition.cloudText,
          weatherText:theForecast.list[i].weather[0].description
        }
        
        // PASS weather data object to template via the variable "fullText"
        var fullText = template(weatherData);
    
        // APPEND fullText to the div.container
        $('.container').append(fullText);
      }
    };
    
    // Function: Call api.openweathermap.com
    var APICall = function(theCity) {
      // get API url
      var weatherUrl = "https://api.openweathermap.org/data/2.5/forecast/daily?q=" + theCity;
      // get API key
      var apiKey = "b0b34e0501286ae903bab8dde901b6ae";
      // get "unit" as imperial
      var unitType = "imperial";
      // get "cnt" as number of days up to 16 days
      var daysTotal = 8;
    
      // start jQuery-based API Call
      $.get({
        url: weatherUrl + "&APPID=" + apiKey + "&units=" + unitType + "&cnt=" + daysTotal,
        success: function(objectFromOWM){
          getWeather(objectFromOWM);
         // console.log(objectFromOWM);
        },
        error: function(response){
         // console.log(response);
        }
      });
    
    };
    
    // On button click, invoke APICall() and pass input text box value
    $('#getWeather').on('click', function(e){
    
      // prevent natural form submit event
      e.preventDefault();
      // check to see if search box has value
      if( $('#city-name').val().trim() === "" || $('#city-name').val().trim() === null ) {
        // if search box is empty, do nothing
        return;
      } else {
        //  clear old results
        $('.section').remove();
    
        // get input box value and invoke APICall function
        var cityName = $('#city-name').val().trim();
        $('#city-name').val("");
        APICall(cityName);
      }
    });
  });

  //farm map 
  var map;
  var resourcemap;
  var icon = ""
  function initialize() {
    var infowindow = new google.maps.InfoWindow();
    var mapProp = {
      center: new google.maps.LatLng(1.0609637, 32.5672804), 
      zoom: 8,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
  
    map = new google.maps.Map(document.getElementById("map"), mapProp);
    resourcemap = new google.maps.Map(document.getElementById("resourcemap"), mapProp);

   //FARMS
    $.getJSON('/farm/api/maps/', function(json) {
      var farmdata = [];
      json.forEach(function (p) {
        p.z = p.land_occupied;
        farmdata.push(p);
      })
      //console.log(farmdata)
  
    $.each(farmdata, function(key, data) {
  
      var latlon = new google.maps.LatLng(data.lat, data.lon);
      //console.log(data)
      var marker = new google.maps.Marker({
        position: latlon,
        map: map,
        //icon: icon,
        data: data.farm_name
      });
  
      
      var details = "REGION:" + data.region + "<br>" + "DISTRICT:" +
      data.district + "<br>" + "FARMER:" + data.farmer + "<br>" + "PHONE NUMBER:" + data.phone_number + "."+"<br>" 
      +'<a style="color:blue;" href="/farm/'+ data.id +'/view/">Farm Details</a>';
  
      bindInfoWindow(marker, map, infowindow, details);
  
      });
  
    });

    //RESOURCES
    $.getJSON('/resourcesharing/api/resource/', function(json) {
      var resourcedata = [];
      json.forEach(function (p) {
        p.z = p.id;
        resourcedata.push(p);
      })
      //console.log(farmdata)
  
    $.each(resourcedata, function(key, data) {
  
      var latlon = new google.maps.LatLng(data.lat, data.lon);
      console.log(data)
      var marker = new google.maps.Marker({
        position: latlon,
        map: resourcemap,
        //icon: icon,
        data: data.resource_name
      });
  
      
      var details = "OWNER:" + data.owner + "<br>" + "PHONE NUMBER:" +
      data.Phone_number1 + "<br>" + "STATUS:" + data.resource_status + "<br>" + "PRICE:" + data.price + ".";
  
      bindInfoWindow(marker, resourcemap, infowindow, details);
  
      });
  
    });
  
  }
  
  function bindInfoWindow(marker, map, infowindow, strDescription) {
    google.maps.event.addListener(marker, 'mouseover', function() {
      infowindow.setContent(strDescription);
      infowindow.open(map, marker);
    });
}

  google.maps.event.addDomListener(window, 'load', initialize);


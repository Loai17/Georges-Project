$(document).ready(function() {
    debugger;
});

var new_marker = null;
var LOCATION;
var NEW_LESSONS = 0;

$.get("http://ip-api.com/json", function(response) {
    LOCATION = [response.lat, response.lon];
}, "jsonp");

var map;
        function initMap() {
        	if (LOCATION != null){
	          map = new google.maps.Map(document.getElementById("map-div"), {
	            center: { lat: LOCATION[0], lng: LOCATION[1] },
	            zoom: 9
	          });
	      }
	      else{map = new google.maps.Map(document.getElementById("map-div"), {
	            center: { lat: 0, lng: 0 },
	            zoom: 2
	          });

	      }

          map.addListener('click', function(p){

          	if(new_marker!=null){
          		new_marker.setMap(null);
          		new_marker=null;
          	}

          	new_marker = new google.maps.Marker({position:p.latLng,map:map});
          	get_air_quality(p.latLng);
          });
        }

async function get_air_quality(position){
	var api_url = "https://api.breezometer.com/air-quality/v2/current-conditions?lat="+position.lat()+"&lon="+position.lng()+"&key=61a13feb9eec4739bc1d423f4e2aa609"
	var response = await fetch(api_url);
	var data = await response.json();

	var text_area = document.getElementById('map_title');

	if (data.data != null){
		var air_q = data.data.indexes.baqi.aqi;
		var text_color = data.data.indexes.baqi.color;
		var cat = data.data.indexes.baqi.category;

		text_area.innerHTML = air_q+', '+cat;
		text_area.style.color = text_color;
	}
	else{
		text_area.innerHTML = "No Data";
		text_area.style.color = '#DDDDDD';
	}

}

async function get_weather(lat,lon){
	var api_url = "https://api.breezometer.com/weather/v1/current-conditions?lat="+lat+"&lon="+lon+"&key=61a13feb9eec4739bc1d423f4e2aa609"
	var response = await fetch(api_url);
	var data = await response.json();

	document.getElementById("date").innerHTML += " - " + data.data.temperature.value + " C&#730;";
}

async function update_weekday(){
	var weekdays = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
	var d = new Date();
	document.getElementById("weekday").innerHTML= weekdays[d.getDay()];
	document.getElementById("date").innerHTML = (d.getDate()+'/'+(d.getMonth()+1)+'/'+(d.getYear()+1900));

	await get_weather(LOCATION[0],LOCATION[1]);
}

function show_login(){
	var my_div = document.getElementById("log_in");
	my_div.style.display = "block";

	var other_div = document.getElementById("sign_up");
	other_div.style.display = "none";
}

function show_signup(){
	var my_div = document.getElementById("sign_up");
	my_div.style.display = "block";

	var other_div = document.getElementById("log_in");
	other_div.style.display = "none";
}

function show_add_assignment(){
	var my_div = document.getElementById("add_assignment_form");
	var other_div = document.getElementById("opaque_div");
	other_div.style.display = "block";
	my_div.style.display = "block";
}

function show_add_lessons(){
	var my_div = document.getElementById("add_lessons_form");
	var other_div = document.getElementById("opaque_div");
	other_div.style.display = "block";
	my_div.style.display = "block";
}

function hide_add_lessons(){
	var my_div = document.getElementById("add_lessons_form");
	var other_div = document.getElementById("opaque_div");
	other_div.style.display = "none";
	my_div.style.display = "none";
}

function hide_add_assignment(){
	var my_div = document.getElementById("add_assignment_form");
	var other_div = document.getElementById("opaque_div");
	other_div.style.display = "none";
	my_div.style.display = "none";
}

function show_add_subject(){
	var my_div = document.getElementById("add_subject_form");
	var other_div = document.getElementById("opaque_div");
	other_div.style.display = "block";
	my_div.style.display = "block";
}

function hide_add_subject(){
	var my_div = document.getElementById("add_subject_form");
	var other_div = document.getElementById("opaque_div");
	other_div.style.display = "none";
	my_div.style.display = "none";
}

function update_lessons_by_day(){
	var sel_elem = document.getElementById("weekday_select");
	var days = document.getElementsByClassName("day_lessons");
	var exc = document.getElementById("day"+sel_elem.value);

	for (var i = days.length - 1; i >= 0; i--) {
		days[i].style.display = "none";
	}

	exc.style.display = "block";
}

function sort_assignments(){
	radios = document.getElementsByName("sort");

	dd = document.getElementById("sorted_by_deadline");
	df = document.getElementById("sorted_by_difficulty");
	sbj = document.getElementById("sorted_by_subject");

	if (radios[0].checked){
		dd.style.display = "block";
		df.style.display = "none";
		sbj.style.display = "none";
	}
	else if (radios[1].checked){
		dd.style.display = "none";
		df.style.display = "block";
		sbj.style.display = "none";	
	}
	else if (radios[2].checked){
		dd.style.display = "none";
		df.style.display = "none";
		sbj.style.display = "block";
	}
}

function show_done(){
	done_assignments = document.getElementsByClassName('done');

	if (document.getElementsByName('show_done')[0].checked){
		for (var i = done_assignments.length - 1; i >= 0; i--) {
			done_assignments[i].style.display = "block";
		}
	}
	else{
		for (var i = done_assignments.length - 1; i >= 0; i--) {
			done_assignments[i].style.display = "none";
		}
	}
}

function open_map(){
	var my_div = document.getElementById("map_box");
	var other_div = document.getElementById("opaque_div");
	other_div.style.display = "block";
	my_div.style.display = "block";
}

function close_map(){
	if(new_marker!=null){
        new_marker.setMap(null);
        new_marker=null;
    }

    var text_area = document.getElementById('map_title');
    text_area.innerHTML = 'Check Air Quality ';
    text_area.style.color = '#F7567C';

    var my_div = document.getElementById("map_box");
	var other_div = document.getElementById("opaque_div");
	other_div.style.display = "none";
	my_div.style.display = "none"; 

}
jQuery(document).ready(function($) {
	
// Select nav for smaller resolutions
// Select menu for smaller screens
$("<select />").appendTo("nav#primary");

// Create default option "Menu"
$("<option />", {
   "selected": "selected",
   "value"   : "",
   "text"    : "Menu"
}).appendTo("nav#primary select");

// Populate dropdown with menu items
$("nav#primary a").each(function() {
 var el = $(this);
 $("<option />", {
     "value"   : el.attr("href"),
     "text"    : el.text()
 }).appendTo("nav select");
});

$("nav#primary select").change(function() {
  window.location = $(this).find("option:selected").val();
});

// Tipsy
$('.tooltip').tipsy({
	gravity: $.fn.tipsy.autoNS,
	fade: true,
	html: true
});

$('.tooltip-s').tipsy({
	gravity: 's',
	fade: true,
	html: true
});

$('.tooltip-e').tipsy({
	gravity: 'e',
	fade: true,
	html: true
});

$('.tooltip-w').tipsy({
	gravity: 'w',
	fade: true,
	html: true
});

// Scroll
jQuery.localScroll();

// Prettyprint
$('pre').addClass('prettyprint linenums');

// Uniform
$("select, input:checkbox, input:radio, input:file").uniform();
	
// Navigation via router events
var WorkspaceRouter = Backbone.Router.extend({
	routes: {
		"/":             	"home",   
		"udh-scale":        "udh",  
		"uxc-scale": 		"uxc", 
		"mts": 				"mts",
		"trails": 			"trails",
		"contact": 			"contact,"
	},
	
	home: function() {
	  console.log("welcome home.");
	},
	
	udh: function() {
	  console.log("udh");
	},
	
	uxc: function() {
		console.log("uxc");
	},
	
	mts: function() {
		console.log("mts");
	},
	
	trails: function() {
		console.log("trails");
	},
	
	contact: function() {
		console.log("contact");
	}
});

$('nav>ul>li>a').click(function(e) {
	// this might cause issues with the back function in IE
    e.preventDefault();
    router.navigate($(this).attr('href'), true )
});

var router = new WorkspaceRouter();
Backbone.history.start();

});

require.config({
  shim: {
    "jquery-serializeForm": ["jquery"],
    "jquery-md5": ["jquery"],
    "jquery-tipsy": ['jquery'],
    "sidr": ['jquery'],
    MathJax: {exports: "MathJax"},
    OpenLayers: {exports: "OpenLayers"}
  },
  paths: {
    sidr: "../libs/sidr/jquery.sidr.min",
    MathJax: "../libs/MathJax/MathJax.js?config=MML_HTMLorMML",
    backbone: "../libs/backbone/backbone",
    "backbone-validation": "../libs/backbone-validation/dist/backbone-validation",
    chart: "../libs/chartjs/Chart.min",
    jquery: "../libs/jquery/dist/jquery",
    "jquery-cookie": "../libs/jquery-cookie/jquery.cookie",
    "jquery-tipsy": "../libs/tipsy/src/javascripts/jquery.tipsy",
    "jquery_scrollto": "../libs/jquery.scrollTo/jquery.scrollTo.min",
    "jquery_localscroll": "../libs/jquery.localScroll/jquery.localScroll.min",
    "jquery-form": "../libs/jquery-form/jquery.form",
    "jquery-touchswipe": "../libs/jquery-touchswipe/jquery.touchSwipe.min",
    modernizr: "../libs/modernizr/modernizr",
    requirejs: "../libs/requirejs/require",
    "backbone-routefilter": "../libs/routefilter/dist/backbone.routefilter.min",
    scrollReveal: "../libs/scrollReveal/dist/scrollReveal",
    text: "../libs/text/text",
    underscore: "../libs/underscore/underscore",
    "scrollReveal": "../libs/scrollReveal/dist/scrollReveal.min",
    OpenLayers:  "../libs/openlayers/OpenLayers"
  },
  packages: [

  ]
});

require([
	'app',
    ], function(App){
		App.initialize();
	}
);

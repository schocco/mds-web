require.config({
  shim: {
    "jquery-tipsy": ['jquery'],
    "sidr": ['jquery'],
    "MathJax": {exports: "MathJax"},
    "OpenLayers": {exports: "OpenLayers"}
  },
  paths: {
    "backbone": "../libs/backbone/backbone",
    "backbone-routefilter": "../libs/routefilter/dist/backbone.routefilter.min",
    "backbone-validation": "../libs/backbone-validation/dist/backbone-validation",
    "chart": "../libs/chartjs/Chart.min",
    "jquery-cookie": "../libs/jquery-cookie/jquery.cookie",
    "jquery-form": "../libs/jquery-form/jquery.form",
    "jquery": "../libs/jquery/dist/jquery",
    "jquery_localscroll": "../libs/jquery.localScroll/jquery.localScroll.min",
  //  "jquery_scrollto": "../libs/jquery.scrollTo/jquery.scrollTo.min",
    "jquery-tipsy": "../libs/tipsy/src/javascripts/jquery.tipsy",
    "jquery-touchswipe": "../libs/jquery-touchswipe/jquery.touchSwipe.min",
    "MathJax": "../libs/MathJax/MathJax.js?config=MML_HTMLorMML",
    "modernizr": "../libs/modernizr/modernizr",
    "OpenLayers":  "../libs/openlayers/OpenLayers",
    "requirejs": "../libs/requirejs/require",
    "scrollReveal": "../libs/scrollReveal/dist/scrollReveal.min",
    "sidr": "../libs/sidr/jquery.sidr.min",
    "text": "../libs/text/text",
    "underscore": "../libs/underscore/underscore"
  }
});

require([
    'app'
    ], function(App){
		App.initialize();
	}
);

//http://tech.pro/blog/1639/using-rjs-to-optimize-your-requirejs-project

( {
    mainConfigFile : 'js/app/config.js',
    baseUrl : "js/app",
    dir : "js/dist",
    inlineText : true,
    removeCombined : true,
    findNestedDependencies : true,
    paths : {
        "MathJax" : "empty:"
    },
    modules : [{
        name : "config",
        exclude : ["MathJax", "OpenLayers"]
    }, {
        name : "infrastructure"
    }]
})

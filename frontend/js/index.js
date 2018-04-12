var map = AmCharts.makeChart( "chartdiv", {
  "type": "map",
  "theme": "light",
  "dataProvider": {
    "map": "worldLow",
    "areas": [ {"id": "FR"},{"id": "LV"},{"id": "ES"},{"id": "AR"},{"id": "AU"},
              {"id": "AT"},{"id": "BE"},{"id": "BO"},{"id": "BR"},{"id": "BG"},
              {"id": "CA"},{"id": "CL"},{"id": "CR"},{"id": "CY"},{"id": "CZ"},
              {"id": "DK"},{"id": "DO"},{"id": "EC"},{"id": "SV"},{"id": "EE"},
              {"id": "FI"},{"id": "DE"},{"id": "GR"},{"id": "GT"},{"id": "HN"},
              {"id": "HK"},{"id": "HU"},{"id": "IS"},{"id": "IE"},{"id": "IT"},
              {"id": "LT"},{"id": "MY"},{"id": "MX"},{"id": "NL"},{"id": "NZ"},
              {"id": "NI"},{"id": "NO"},{"id": "PA"},{"id": "PY"},{"id": "PE"},
              {"id": "PH"},{"id": "PL"},{"id": "PT"},{"id": "SG"},{"id": "SK"},
              {"id": "SE"},{"id": "CH"},{"id": "TW"},{"id": "TR"},{"id": "GB"},
              {"id": "UY"},{"id": "US"}
            ]
  },
  "areasSettings": {
    "autoZoom": true,
    "selectedColor": "#CC0000"
  },
  "listeners": [ {
    "event": "clickMapObject",
    "method": function( e ) {
      // check if clicked map object contains "ajaxUrl" parameter
      if ( e.mapObject.id !== undefined ) {
        // add "description" if it was empty

        console.log(e.mapObject.id);
        var countryUrl = ajaxUrlGenerator(e.mapObject.id);
        console.log(countryUrl);
        if ( e.mapObject.description === undefined )
          e.mapObject.description = "<div id='mapcontent'>Loading...</div>";

            // Parse JSON
          AmCharts.loadFile( countryUrl, {}, function( response ) {
            console.log(response);
            var data = AmCharts.parseJSON( response, {
              "useColumnNames": true
            } );
            var sec = Math.floor(data.duration / 1000);
            var min =  Math.floor(sec / 60);
            sec = sec % 60;
            console.log("data.genres.count " + data.genres.length);
              e.mapObject.description = "GDP: " + data.gdp +
                                  "</br> GDP per capital: " + data.gdpPerCapita +
                                  "</br> GINI index: " + data.gini +
                                  "</br> HDI: " + data.hdi +
                                  "</br> HDI Rank " + data.hdiRank +
                                  "</br> Population density: " + data.populationDensity +
                                  "</br> Average song length: " + min + "," + sec;
          });
      }
    }
  } ]
} );


function ajaxUrlGenerator(countryID) {
  if (countryID === "GB"){
    return "http://87d08036.ngrok.io/" + "UK" + "/";
  } else {
    return "http://87d08036.ngrok.io/" + countryID + "/";
  }
};

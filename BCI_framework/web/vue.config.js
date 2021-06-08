const path = require("path");

module.exports = {
  // holds the folder for the static files (css, js etc).
  // Note It is relative to the value provided in the outputDir field.

  // Please comment this line under developing
  assetsDir: "../../static",
  // baseUrl: '',

  //  hold the path prefix for the static files in the index.html.
  publicPath: "",

  // This folder holds the location of the built vue files
  // the folder that will hold the index.html that wil load the vue app
  // If you observe the path provided, you'll notice that the folder is inside the app module of the flask application.
  
  outputDir: path.resolve(__dirname, "../library/templates/vue"),

  runtimeCompiler: undefined,

  productionSourceMap: undefined,

  parallel: undefined,

  css: undefined,
};

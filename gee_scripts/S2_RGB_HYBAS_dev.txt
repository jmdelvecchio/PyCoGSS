// Set the date for the imagery
// Pick the "best" date in ImageCollection -> features
var imageDate = ee.Date('2020-5-21')

var HYBAS_ID=3100133910

var shed = ee.FeatureCollection("WWF/HydroSHEDS/v1/Basins/hybas_10")
.filter(ee.Filter.eq('HYBAS_ID', HYBAS_ID))

print(shed.first())
// print(shed.toDictionary().values())
// to do: grab hybas id as client side string for export

Map.addLayer(shed, false)

var centroid = shed.geometry().centroid()
var geometry = centroid.buffer({'distance': 20000})
Map.addLayer(geometry, false)
// Map.setCenter(
//   shed.geometry().centroid().coordinates().get(0).getInfo(),
//   shed.geometry().centroid().coordinates().get(1).getInfo(),
//   11)
// I am proud of this one lol
Map.centerObject(centroid, 11) 

function maskS2clouds(image) {
  var qa = image.select('QA60');

  // Bits 10 and 11 are clouds and cirrus, respectively.
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11;

  // Both flags should be set to zero, indicating clear conditions.
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
      .and(qa.bitwiseAnd(cirrusBitMask).eq(0))
      ;

  return image.updateMask(mask)
  .divide(10000)
  .copyProperties(image, ['system:time_start']);
}
function clp(img) {
  return img.clip(shed)
}////
function mosaicByDate(imcol){
  // imcol: An image collection
  // returns: An image collection
  var imlist = imcol.toList(imcol.size())

  var unique_dates = imlist.map(function(im){
    return ee.Image(im).date().format("YYYY-MM-dd")
  }).distinct()

  var mosaic_imlist = unique_dates.map(function(d){
    d = ee.Date(d)

    var im = imcol
      .filterDate(d, d.advance(1, "day"))
      .mosaic()

    return im.set(
        "system:time_start", d.millis(), 
        "system:id", d.format("YYYY-MM-dd"))
  })

  return ee.ImageCollection(mosaic_imlist)
}
////
function addNDWI(image) {
  var ndwi = image.normalizedDifference(['B3', 'B8A']).rename('NDWI');
  return image.addBands(ndwi);
};
function addNDVI(image) {
  var ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI');
  return image.addBands(ndvi);
};
////
var dataset = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                  .filter(ee.Filter.calendarRange(2019,2019,'year'))
                  .filter(ee.Filter.calendarRange(5,8,'month'))
                  // Pre-filter to get less cloudy granules.
                  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
                  .filterBounds(shed.geometry().centroid())
                  // .filter(ee.Filter.contains('.geo', shed))
                  .map(clp)
                  .map(maskS2clouds);

var dataset = mosaicByDate(dataset).map(addNDWI).map(addNDVI)

print(dataset)

var ndwiParams = {min: -1, max: 1, palette: ['yellow', 'blue']};
var ndviViz = {palette: 'brown, blanchedalmond, #8FBC8F, #006400',};

var s2Params = {min: -1, max: 1, palette: ['black', 'white']};

var varParams = {min: -1, max: 4, palette: ['black', 'white']};

var rgbViz = {
  min: 0.0,
  max: 0.1,
  bands: ['B4', 'B3', 'B2'],
};
//*

Map.addLayer(dataset.select('NDVI'), s2Params, 'NDVI', false);
Map.addLayer(dataset.select('NDWI'), s2Params, 'NDWI', false);

Map.addLayer(dataset.filterDate(imageDate), rgbViz, 'RBG')

var ndwi_st = dataset.select('NDWI')
.reduce(ee.Reducer.kurtosis())
Map.addLayer(ndwi_st, varParams, 'NDWI_stdev', false);

var imageRGB = dataset.filterDate(imageDate).first().visualize(rgbViz)
var imageNDVI = dataset.select('NDVI').filterDate(imageDate).first().visualize(s2Params)
var imageNDWI = dataset.select('NDWI').filterDate(imageDate).first().visualize(s2Params)
var imageNDWI_stdev = ndwi_st.visualize(s2Params)

Export.image.toDrive({
  image: imageRGB,
// Don't forget to change these!!!!!
  description: ee.String(HYBAS_ID.toString()).cat('_rgb').getInfo(),
  folder: "random_state_2",
// Change me!!!
	region: geometry,
  scale: 10,
  fileDimensions: 512, // you can change this
  skipEmptyTiles: true,
  crs: 'EPSG:5936', //polar
  //maxPixels: 1e13
  maxPixels: 163164208
})

Export.image.toDrive({
  image: imageNDVI,
// Don't forget to change these!!!!!
  description: ee.String(HYBAS_ID.toString()).cat('_ndvi').getInfo(),
  folder: HYBAS_ID.toString(),
// Change me!!!
	region: geometry,
  scale: 10,
  fileDimensions: 1024, // you can change this
  skipEmptyTiles: true,
  crs: 'EPSG:5936', //polar
  //maxPixels: 1e13
  maxPixels: 163164208
})

Export.image.toDrive({
  image: imageNDWI,
// Don't forget to change these!!!!!
  description: ee.String(HYBAS_ID.toString()).cat('_ndwi').getInfo(),
  folder: HYBAS_ID.toString(),
// Change me!!!
	region: geometry,
  scale: 10,
  fileDimensions: 1024, // you can change this
  skipEmptyTiles: true,
  crs: 'EPSG:5936', //polar
  //maxPixels: 1e13
  maxPixels: 163164208
})

Export.image.toDrive({
  image: dataset.filterDate(imageDate).first().select('B4', 'B3', 'B2','B8', 'B8A'),
// Don't forget to change these!!!!!
  description: ee.String(HYBAS_ID.toString()).cat('_multiband').getInfo(),
  folder: HYBAS_ID.toString(),
// Change me!!!
	region: geometry,
  scale: 10,
  fileDimensions: 1024, // you can change this
  skipEmptyTiles: true,
  crs: 'EPSG:5936', //polar
  //maxPixels: 1e13
  maxPixels: 163164208
})
Export.table.toDrive({
  collection: shed,
  // Me too!!!!!!
  description: HYBAS_ID.toString(),
  folder: 'random_state_2',
  fileNamePrefix: HYBAS_ID.toString(),
  // Me too!!!!!
  fileFormat: 'SHP'
});




var args = {
  dimensions: '1200x600',
  region: geometry,
  framesPerSecond: 3,
    // crs: 'EPSG:5936', //polar
  min: 0.0,
  max: 0.1,
  bands: ['B4', 'B3', 'B2'],
};
var thumb = ui.Thumbnail({
  image: dataset,
  params: args,
  });

print(thumb)

var listOfImages = dataset.toList(dataset.size()); // 29 images

print(ee.Image(listOfImages.get(0)).date().format('yyyy-MM-dd'))
// client side loop
for(var i = 0; i < 30; i++){
  var image = ee.Image(listOfImages.get(i));
  Map.addLayer(image, rgbViz, 
  ee.Image(image).date().format('yyyy-MM-dd').getInfo(), false
  // i.toString()
  )
}


// var slider = ui.Slider();
// slider.onSlide(function(value) {
//   var int_value = value * (Map.layers().length() - 1) >> 0;
//   Map.layers().get(int_value).setOpacity(1);
//   for (var i = int_value + 1; i < Map.layers().length(); i++) {
//     Map.layers().get(i).setOpacity(0);
// }
// });
// print(slider);

// make a slider
// var slider = ui.Slider({min: 0, 
//                         max: Map.layers().length() - 1, 
//                         value: 0, 
//                         step: 1});
// print(slider);

// slider.onSlide(function(value) {
  
//   // set opacity all layers 0
//   for (var i = 0; i < Map.layers().length(); i++) {
//     Map.layers().get(i).setOpacity(0);
//   }
  
//   // set opacity slided layer to 1
//   Map.layers().get(value).setOpacity(1);
// });
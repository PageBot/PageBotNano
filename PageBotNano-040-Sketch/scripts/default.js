console.log('This is an example Sketch script.')

var sketch = require('sketch')

var document = sketch.getSelectedDocument()

var selectedLayers = document.selectedLayers
var selectedCount = selectedLayers.length

if (selectedCount === 0) {
  console.log('No layers are selected.')
} else {
  console.log('Selected layers:');
  selectedLayers.forEach(function (layer, i) {
    console.log((i + 1) + '. ' + layer.name)
  })
}

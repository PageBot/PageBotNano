          var onRun = function(context) {
          

/*
	second draw
*/

let sketch = require('sketch')
let document = sketch.getSelectedDocument()
let page = document.selectedPage
page.layers = []
let Artboard = sketch.Artboard
let myArtboard = new Artboard({
    parent: page,
    frame: { x: 0, y: 0, width: 400, height: 400 }
})
/* SketchApp version XXX

let ShapePath = sketch.ShapePath

*/

/* SketchApp version XXX */

var ShapePath = require('sketch/dom').ShapePath
/*let ShapePath = sketch.Shape*/

/*
console.log(ShapePath.ShapeType)
*/

let mySquare1 = new ShapePath({
    parent: myArtboard,
    frame: { x: 53, y: 213, width: 122, height: 122 },
    style: { fills: ['#35E6C9']}
})


let mySquare2 = new ShapePath({
    parent: myArtboard, 
    frame: { x: 253, y: 213, width: 122, height: 122 },
    style: { fills: ['#d5ffb3']}
})

let mySquare3 = new ShapePath({
    parent: myArtboard, 
    frame: { x: 253, y: 313, width: 50, height: 50 },
    style: { fills: ['#0000DD']}
})


let myCircle1 = new ShapePath({
    shapeType: ShapePath.ShapeType.Oval,
    parent: myArtboard, 
    frame: { x: 253, y: 213, width: 122, height: 122 },
    style: { fills: ['#FF0000'], borders: [{color: '#00FF00',thickness: 16}]}
})

/*

console.log(mySquare2)

*/

var Text = require('sketch/dom').Text

console.log(Text)



          };
          
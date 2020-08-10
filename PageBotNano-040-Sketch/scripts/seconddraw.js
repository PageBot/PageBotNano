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

console.log(mySquare2)


/*
	firstdraw.js
*/


let sketch = require('sketch')
let document = sketch.getSelectedDocument()
console.log(document)
let page = document.selectedPage
page.layers = [] /* Clear all Artboards */
console.log(page)
let Artboard = sketch.Artboard
let myArtboard = new Artboard({
	parent: page,
	frame: { x: 0, y: 0, width: 400, height: 400 },
	name: 'My Artboard Name'
})

/*
myArtboard.parent = page
myArtboard.frame = { x: 0, y: 0, width: 400, height: 400 }
myArtboard.name = 'My Artboard Name'
*/

let ShapePath = sketch.ShapePath
let mySquare = new ShapePath({
    parent: myArtboard, 
    frame: { x: 53, y: 213, width: 122, height: 122 },
    style: { fills: ['#35E6C9']}
})

/*
console.log(myArtboard)

console.log(context)

*/
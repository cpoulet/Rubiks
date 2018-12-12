import { Cube } from  "./cube.js";

const STEP = 32;
const VERBOSE = true;

var pressed = false;
var stack = [];

var Rubiks;
var scene;

// shift = 16
function keyDownHandler(event) {
    if (pressed == true) {return;}
    pressed = true;
    let i = event.keyCode;
    if (i == 70) {
        stack.unshift('F');
    } else if (i == 82) {
        stack.unshift('R');
    } else if (i == 85) {
        stack.unshift('U');
    } else if (i == 66) {
        stack.unshift('B');
    } else if (i == 76) {
        stack.unshift('L');
    } else if (i == 68) {
        stack.unshift('D');
    }
}

function keyUpHandler(event) {
    pressed = false;
}

function createScene(canvas, engine) {
    const scene = new BABYLON.Scene(engine);
    
    var camera = new BABYLON.ArcRotateCamera("Camera", 3 * Math.PI / 4, Math.PI / 4, 10, BABYLON.Vector3.Zero(), scene);
    camera.attachControl(canvas, true);

    var light1 = new BABYLON.HemisphericLight("light1", new BABYLON.Vector3(1, 1, 0), scene);
    var light2 = new BABYLON.HemisphericLight("light3", new BABYLON.Vector3(0, -1, 0), scene);

    return scene;
}

function reset() {
    var req = new XMLHttpRequest();

    req.onreadystatechange = function(e) {
        if (req.readyState == 4 && req.status == 200) {
            if (VERBOSE) {
                console.log('Reset');
            }
            Rubiks.reset();
        }
    }
    req.open('POST', '/reset', true);
    req.send();
}

function mix() {
    var req = new XMLHttpRequest();

    req.onreadystatechange = function(e) {
        if (req.readyState == 4 && req.status == 200) {
            let sequence = JSON.parse(req.responseText);
            if (VERBOSE) {
                console.log(sequence);
            }
            for (let i=0; i < sequence.length; i++) {
                stack.unshift(sequence[i]);
            }
        }
    }
    req.open('POST', '/mix', true);
    req.send();
}

function main() {
    document.querySelector("#mix").addEventListener("click", mix);
    document.querySelector("#reset").addEventListener("click", reset);

    const canvas = document.querySelector('#cube');
    const engine = new BABYLON.Engine(canvas, true);
    scene = createScene(canvas, engine);

    Rubiks = new Cube(scene, STEP);
    
    document.addEventListener('keydown', keyDownHandler, false);
    document.addEventListener('keyup', keyUpHandler, false);

    scene.registerBeforeRender(function() {
        if (Rubiks.moving) {
            Rubiks.move();
        } else {
            let m = stack.pop();
            Rubiks.nextMove(m);
        }
    });

    engine.runRenderLoop(function() {
        scene.render();
     });
}

main();

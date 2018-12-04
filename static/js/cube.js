const STEP = 32;
const VERBOSE = true;

var pressed = false;
var stack = [];

//testArchi();
//testVisu();
main();

function testVisu() {
    const canvas = document.querySelector('#cube');
    const engine = new BABYLON.Engine(canvas, true);
    let scene = createScene(canvas, engine);

    let Rubiks = createRubiks(scene);

    let f = [0,1,2,3,4,5,6,7,8];
    for (i in f) {
        Rubiks[f[i]].setParent(Rubiks[13]);
    }
    Rubiks[13].rotate(BABYLON.Axis.Z, Math.PI / 4, BABYLON.Space.WORLD);

    engine.runRenderLoop(function() {
        scene.render();
     });
}

function testArchi() {
    let archi = createArchi();
    show(archi)
    let stack = ['L', 'L', 'L', 'L'].reverse();
    let move = stack.pop();
    while (move) {
        updateArchi(archi, move);
        move = stack.pop();
    }
}

function main() {
    const canvas = document.querySelector('#cube');
    const engine = new BABYLON.Engine(canvas, true);
    let scene = createScene(canvas, engine);

    let Rubiks = createRubiks(scene);
    let archi = createArchi();
    if (VERBOSE) {
        show(archi)
    }
    
    document.addEventListener('keydown', keyDownHandler, false);
    document.addEventListener('keyup', keyUpHandler, false);

    let i = 0;
    let pending = false;
    scene.registerBeforeRender(function() {
        if (pending) {
            if (i == STEP / 2) {
                i = 0;
                pending = false;
            } else {
                window[move[0]](Rubiks, archi, move.length);
                i++;
            }
        } else {
            move = nextMove(stack, Rubiks, archi);
            pending = move ? true : false;
        }
    });

    engine.runRenderLoop(function() {
        scene.render();
     });
}

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

function nextMove(stack, Rubiks, archi) {
    let move = stack.pop();
    if (move) {
        let dir = move.length == 1 ? 1 : -1;
        if (VERBOSE) {
            console.log("_____", move, "_____");
        }
        setParents(Rubiks, move[0], archi);
        updateArchi(archi, move[0], dir);
        if (VERBOSE) {
            show(archi);
        }
        return move;
    }
    return false;
}

function updateArchi(archi, move, dir) {
    let tmp = archi.slice(0);
    if (dir == 1) {
        window['rot' + move](archi, tmp);
    } else {
        prime(archi, tmp, 'rot' + move);
    }
}

function setParents(Rubiks, move, archi) {
    let set = new Set(window['get' + move](archi));
    for (let i = 0; i < 27; i++) {
        if (set.has(i)) {
            Rubiks[i].setParent(Rubiks[13]);
        } else {
            Rubiks[i].setParent(null);
        }
    }
}

function U(Rubiks, archi, dir) {
    dir = dir == 1 ? dir : -1;
    Rubiks[13].rotate(BABYLON.Axis.Y, dir * Math.PI / STEP, BABYLON.Space.WORLD);
}

function D(Rubiks, archi, dir) {
    dir = dir == 1 ? dir : -1;
    Rubiks[13].rotate(BABYLON.Axis.Y, dir * -Math.PI / STEP, BABYLON.Space.WORLD);
}

function F(Rubiks, archi, dir) {
    dir = dir == 1 ? dir : -1;
    Rubiks[13].rotate(BABYLON.Axis.Z, dir * Math.PI / STEP, BABYLON.Space.WORLD);
}

function B(Rubiks, archi, dir) {
    dir = dir == 1 ? dir : -1;
    Rubiks[13].rotate(BABYLON.Axis.Z, dir * -Math.PI / STEP, BABYLON.Space.WORLD);
}

function L(Rubiks, archi, dir) {
    dir = dir == 1 ? dir : -1;
    Rubiks[13].rotate(BABYLON.Axis.X, dir * Math.PI / STEP, BABYLON.Space.WORLD);
}

function R(Rubiks, archi, dir) {
    dir = dir == 1 ? dir : -1;
    Rubiks[13].rotate(BABYLON.Axis.X, dir * -Math.PI / STEP, BABYLON.Space.WORLD);
}

function createArchi() {
    let archi = [];
    for (let i = 0; i < 27; i++) {
        archi.push(i);
    }
    return archi;
}

function getF(cube) {return cube.slice(0,9);}
function getB(cube) {return cube.slice(18,);}
function getU(cube) {return cube.filter(function(v, i) {return i % 9 < 3});}
function getD(cube) {return cube.filter(function(v, i) {return i % 9 >= 6});}
function getL(cube) {return cube.filter(function(v, i) {return i % 3 == 0});}
function getR(cube) {return cube.filter(function(v, i) {return i % 3 == 2});}

function prime(archi, tmp, foo) {
    for (let i=0; i < 3; i++) {
        window[foo](archi, tmp);
        tmp = archi.slice(0);
    }
}

// 18 19 20
//  9 10 11
//  0  1  2
//
//  0  9 18
//  1 10 19
//  2 11 20
function rotU(archi, tmp) {
    archi[0] = tmp[2];
    archi[1] = tmp[11];
    archi[2] = tmp[20];
    archi[11] = tmp[19];
    archi[20] = tmp[18];
    archi[19] = tmp[9];
    archi[18] = tmp[0];
    archi[9] = tmp[1];
}

//  6  7  8
// 15 16 17
// 24 25 26
//
// 24 15  6
// 25 10  7
// 26 17  8
function rotD(archi, tmp) {
    archi[6] = tmp[24];
    archi[7] = tmp[15];
    archi[8] = tmp[6];
    archi[17] = tmp[7];
    archi[26] = tmp[8];
    archi[25] = tmp[17];
    archi[24] = tmp[26];
    archi[15] = tmp[25];
}

// 0 1 2
// 3 4 5
// 6 7 8
//
// 6 3 0
// 7 4 1
// 8 5 2
function rotF(archi, tmp) {
    archi[0] = tmp[6];
    archi[1] = tmp[3];
    archi[2] = tmp[0];
    archi[5] = tmp[1];
    archi[8] = tmp[2];
    archi[7] = tmp[5];
    archi[6] = tmp[8];
    archi[3] = tmp[7];
}

// 20 19 18
// 23 22 21
// 26 25 24
//
// 26 23 20
// 25 22 19
// 24 21 18
function rotB(archi, tmp) {
    archi[20] = tmp[26];
    archi[19] = tmp[23];
    archi[18] = tmp[20];
    archi[21] = tmp[19];
    archi[24] = tmp[18];
    archi[25] = tmp[21];
    archi[26] = tmp[24];
    archi[23] = tmp[25];
}

//  2 11 20
//  5 14 23
//  8 17 26
//
//  8  5  2
// 17 14 11
// 26 23 20
function rotR(archi, tmp) {
    archi[2] = tmp[8];
    archi[11] = tmp[5];
    archi[20] = tmp[2];
    archi[23] = tmp[11];
    archi[26] = tmp[20];
    archi[17] = tmp[23];
    archi[8] = tmp[26];
    archi[5] = tmp[17];
}

// 18  9  0
// 21 12  3
// 24 15  6
//
// 24 21 18
// 15 12  9
//  6  3  0
function rotL(archi, tmp) {
    archi[18] = tmp[24];
    archi[9] = tmp[21];
    archi[0] = tmp[18];
    archi[3] = tmp[9];
    archi[6] = tmp[0];
    archi[15] = tmp[3];
    archi[24] = tmp[6];
    archi[21] = tmp[15];
}

/*
      18 19 20
    9 10 11 23
 0  1  2 14 26
 3  4  5 17
 6  7  8
*/
function show(archi) {
    function nb(i) {
        return String(archi[i]).padStart(2) + ' ';
    }
    console.log(' '.repeat(6) + nb(18) + nb(19) + nb(20));
    console.log(' '.repeat(3) + nb(9) + nb(10) + nb(11) + nb(23));
    console.log(nb(0) + nb(1) + nb(2) + nb(14) + nb(26));
    console.log(nb(3) + nb(4) + nb(5) + nb(17));
    console.log(nb(6) + nb(7) + nb(8));
}

function createRubiks(scene) {

    const pos = [1.05, 0, -1.05];
    let Rubiks = [];
    for (z in pos) {
        for (y in pos) {
            for (x in pos) {
                Rubiks.push(createCube(scene, pos[x], pos[y], pos[z]));
            }
        }
    }
    return Rubiks;
}

function createCube(scene, x, y, z) {
    let faceColors = [
        new BABYLON.Color4(1,0.5,0,1),
        new BABYLON.Color4(1,0,0,1),
        new BABYLON.Color4(0,0,1,1),
        new BABYLON.Color4(0,1,0,1),
        new BABYLON.Color4(1,1,1,1),
        new BABYLON.Color4(1,1,0,1),
    ];
    const black = new BABYLON.Color4(0,0,0,1);
    faceColors[0] = z <= 0 ? black : faceColors[0];
    faceColors[1] = z >= 0 ? black : faceColors[1];
    faceColors[2] = x <= 0 ? black : faceColors[2];
    faceColors[3] = x >= 0 ? black : faceColors[3];
    faceColors[4] = y <= 0 ? black : faceColors[4];
    faceColors[5] = y >= 0 ? black : faceColors[5];
    var box = BABYLON.MeshBuilder.CreateBox("box", {height: 1, width: 1, depth: 1, faceColors : faceColors}, scene);
    box.position.x = x;
    box.position.y = y;
    box.position.z = z;
    return box;
}

function createScene(canvas, engine) {
    const scene = new BABYLON.Scene(engine);
    
    var camera = new BABYLON.ArcRotateCamera("Camera", 3 * Math.PI / 4, Math.PI / 4, 10, BABYLON.Vector3.Zero(), scene);
    camera.attachControl(canvas, true);

    var light1 = new BABYLON.HemisphericLight("light1", new BABYLON.Vector3(1, 1, 0), scene);
    var light2 = new BABYLON.HemisphericLight("light3", new BABYLON.Vector3(0, -1, 0), scene);

    return scene;
}

function mix() {
    var req = new XMLHttpRequest();

    req.onreadystatechange = function(e) {
        if (req.readyState == 4 && req.status == 200) {
            sequence = JSON.parse(req.responseText);
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

/*    moves = ["U","U'","F","F'","R","R'","L","L'","D","D'","B","B'",]
    for (let i=0; i < 20; i++) {
        let move = moves[Math.floor(Math.random()*moves.length)];
        stack.unshift(move);
    }*/
}

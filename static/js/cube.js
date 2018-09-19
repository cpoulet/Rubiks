//testArchi();
//testVisu();
main();

const STEP = 64;

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

function updateArchi(archi, move) {
    window['rot' + move](archi);
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
    show(archi)
    
    let stack = ['F', 'U', 'R', 'R', 'U', 'L'].reverse();
    let i = 0;
    let move = nextMove(stack, Rubiks, archi);
    scene.registerBeforeRender(function() {
        if (move) {
            if (i == STEP / 2) {
                i = 0;
                move = nextMove(stack, Rubiks, archi);
            } else {
                window[move](Rubiks, archi);
                i++;
            }
        }
    });

    engine.runRenderLoop(function() {
        scene.render();
     });
}

function nextMove(stack, Rubiks, archi) {
    let move = stack.pop();
    if (move) {
        console.log("_____", move, "_____");
        setParents(Rubiks, move, archi);
        updateArchi(archi, move);
        show(archi);
        return move;
    }
    return false;
}

function updateArchi(archi, move) {
    let tmp = archi.slice(0);
    window['rot' + move](archi, tmp);
}

function setParents(Rubiks, move, archi) {
    let set = new Set(window['get' + move](archi));
    console.log(set);
    for (let i = 0; i < 27; i++) {
        if (set.has(i)) {
            Rubiks[i].setParent(Rubiks[13]);
        } else {
            Rubiks[i].setParent(null);
        }
    }
}

function U(Rubiks, archi) {
    Rubiks[13].rotate(BABYLON.Axis.Y, Math.PI / STEP, BABYLON.Space.WORLD);
}

function F(Rubiks, archi) {
    Rubiks[13].rotate(BABYLON.Axis.Z, Math.PI / STEP, BABYLON.Space.WORLD);
}

function R(Rubiks, archi) {
    Rubiks[13].rotate(BABYLON.Axis.X, -Math.PI / STEP, BABYLON.Space.WORLD);
}

function L(Rubiks, archi) {
    Rubiks[13].rotate(BABYLON.Axis.X, Math.PI / STEP, BABYLON.Space.WORLD);
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
function getR(cube) {return cube.filter(function(v, i) {return i % 3 == 2});}
function getL(cube) {return cube.filter(function(v, i) {return i % 3 == 0});}

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

const STEP = 32;
const VERBOSE = true;

var pressed = false;
var stack = [];

function testVisu() {
    const canvas = document.querySelector('#cube');
    const engine = new BABYLON.Engine(canvas, true);
    let scene = createScene(canvas, engine);

    let R = new Cube(scene, STEP);

    let f = [0,1,2,3,4,5,6,7,8];
    for (i in f) {
        R.Rubiks[f[i]].setParent(R.Rubiks[13]);
    }
    R.Rubiks[13].rotate(BABYLON.Axis.Z, Math.PI / 4, BABYLON.Space.WORLD);

    engine.runRenderLoop(function() {
        scene.render();
     });
}

function testArchi() {
    let archi = new Archi;
    archi.show();
    let stack = ['L', 'L', 'L', 'L'].reverse();
    let move = stack.pop();
    while (move) {
        archi.updateArchi(move);
        archi.show();
        move = stack.pop();
    }
}

function main() {
    const canvas = document.querySelector('#cube');
    const engine = new BABYLON.Engine(canvas, true);
    let scene = createScene(canvas, engine);

    let Rubiks = new Cube(scene, STEP);
    
    document.addEventListener('keydown', keyDownHandler, false);
    document.addEventListener('keyup', keyUpHandler, false);

    scene.registerBeforeRender(function() {
        if (Rubiks.moving) {
            Rubiks.move();
        } else {
            m = stack.pop();
            Rubiks.nextMove(m);
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

class Archi {
    constructor() {
        this.archi = [];
        for (let i = 0; i < 27; i++) {
            this.archi.push(i);
        }
    }

    updateArchi(move, dir) {
        if (dir == 1) {
            this['rot' + move]();
        } else {
            for (let i=0; i < 3; i++) {
                this['rot' + move]();
            }
        }
    }

    rotU() {
        let tmp = this.archi.slice(0);
        this.archi[0] = tmp[2];
        this.archi[1] = tmp[11];
        this.archi[2] = tmp[20];
        this.archi[11] = tmp[19];
        this.archi[20] = tmp[18];
        this.archi[19] = tmp[9];
        this.archi[18] = tmp[0];
        this.archi[9] = tmp[1];
    }

    rotD() {
        let tmp = this.archi.slice(0);
        this.archi[6] = tmp[24];
        this.archi[7] = tmp[15];
        this.archi[8] = tmp[6];
        this.archi[17] = tmp[7];
        this.archi[26] = tmp[8];
        this.archi[25] = tmp[17];
        this.archi[24] = tmp[26];
        this.archi[15] = tmp[25];
    }

    rotF() {
        let tmp = this.archi.slice(0);
    	this.archi[0] = tmp[6];
    	this.archi[1] = tmp[3];
    	this.archi[2] = tmp[0];
    	this.archi[5] = tmp[1];
    	this.archi[8] = tmp[2];
    	this.archi[7] = tmp[5];
    	this.archi[6] = tmp[8];
    	this.archi[3] = tmp[7];
    }

    rotB() {
        let tmp = this.archi.slice(0);
    	this.archi[20] = tmp[26];
    	this.archi[19] = tmp[23];
    	this.archi[18] = tmp[20];
    	this.archi[21] = tmp[19];
    	this.archi[24] = tmp[18];
    	this.archi[25] = tmp[21];
    	this.archi[26] = tmp[24];
    	this.archi[23] = tmp[25];
    }

    rotR() {
        let tmp = this.archi.slice(0);
    	this.archi[2] = tmp[8];
    	this.archi[11] = tmp[5];
    	this.archi[20] = tmp[2];
    	this.archi[23] = tmp[11];
    	this.archi[26] = tmp[20];
    	this.archi[17] = tmp[23];
    	this.archi[8] = tmp[26];
    	this.archi[5] = tmp[17];
    }

    rotL() {
        let tmp = this.archi.slice(0);
    	this.archi[18] = tmp[24];
    	this.archi[9] = tmp[21];
    	this.archi[0] = tmp[18];
    	this.archi[3] = tmp[9];
    	this.archi[6] = tmp[0];
    	this.archi[15] = tmp[3];
    	this.archi[24] = tmp[6];
    	this.archi[21] = tmp[15];
    }

    show() {
        let archi = this.archi;
        function nb(i) {
            return String(archi[i]).padStart(2) + ' ';
        }
        console.log(' '.repeat(6) + nb(18) + nb(19) + nb(20));
        console.log(' '.repeat(3) + nb(9) + nb(10) + nb(11) + nb(23));
        console.log(nb(0) + nb(1) + nb(2) + nb(14) + nb(26));
        console.log(nb(3) + nb(4) + nb(5) + nb(17));
        console.log(nb(6) + nb(7) + nb(8));
    }
}

class Cube {
    constructor(scene, step) {
        const pos = [1.05, 0, -1.05];
        this.VERBOSE = true;
        this.STEP = step;
        this.i = 0;
        this.moving = false;
        this.scene = scene;
        this.Rubiks = [];
        this.archi = new Archi;
        for (let z in pos) {
            for (let y in pos) {
                for (let x in pos) {
                    this.Rubiks.push(this.createCube(pos[x], pos[y], pos[z]));
                }
            }
        }
    }
    
    createCube(x, y, z) {
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
        var box = BABYLON.MeshBuilder.CreateBox("box", {height: 1, width: 1, depth: 1, faceColors : faceColors}, this.scene);
        box.position.x = x;
        box.position.y = y;
        box.position.z = z;
        return box;
    }

    move() {
        if (this.i == this.STEP / 2) {
            this.i = 0;
            this.moving = false;
        } else {
    	    let dir = this.moving.length == 1 ? 1 : -1;
            this[this.moving[0]](dir);
            this.i++;
        }
    }

    nextMove(move) {
        this.moving = false;
        if (move) {
            this.setParents(move);
            if (this.VERBOSE) {
                console.log("_____", move, "_____");
                this.archi.show();
            }
            this.moving = move;
        }
    }

    setParents(move) {
        let dir = move.length == 1 ? 1 : -1;
        this.archi.updateArchi(move[0], dir);
        let set = new Set(this['get' + move[0]]());
        for (let i = 0; i < 27; i++) {
            if (set.has(i)) {
                this.Rubiks[i].setParent(this.Rubiks[13]);
            } else {
                this.Rubiks[i].setParent(null);
            }
        }
    }

    getF() {return this.archi.archi.slice(0,9);}
    getB() {return this.archi.archi.slice(18,);}
    getU() {return this.archi.archi.filter(function(v, i) {return i % 9 < 3});}
    getD() {return this.archi.archi.filter(function(v, i) {return i % 9 >= 6});}
    getL() {return this.archi.archi.filter(function(v, i) {return i % 3 == 0});}
    getR() {return this.archi.archi.filter(function(v, i) {return i % 3 == 2});}

	U(dir) {this.Rubiks[13].rotate(BABYLON.Axis.Y, dir * Math.PI / STEP, BABYLON.Space.WORLD);}
	D(dir) {this.Rubiks[13].rotate(BABYLON.Axis.Y, dir * -Math.PI / STEP, BABYLON.Space.WORLD);}
	F(dir) {this.Rubiks[13].rotate(BABYLON.Axis.Z, dir * Math.PI / STEP, BABYLON.Space.WORLD);}
	B(dir) {this.Rubiks[13].rotate(BABYLON.Axis.Z, dir * -Math.PI / STEP, BABYLON.Space.WORLD);}
	L(dir) {this.Rubiks[13].rotate(BABYLON.Axis.X, dir * Math.PI / STEP, BABYLON.Space.WORLD);}
	R(dir) {this.Rubiks[13].rotate(BABYLON.Axis.X, dir * -Math.PI / STEP, BABYLON.Space.WORLD);}

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
            //reset();
        }
    }
    req.open('POST', '/reset', true);
    req.send();
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

//testArchi();
//testVisu();
main();

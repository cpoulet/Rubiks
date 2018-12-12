import { Archi } from  "./archi.js";

export class Cube {
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

    reset() {
        const pos = [1.05, 0, -1.05];
        for (let i = 0; i < 27; i++) {
            this.Rubiks[i].dispose();
        }
        this.archi.newCube();
        if (this.VERBOSE) {
            console.log("___Reset___");
            this.archi.show();
        }
        this.Rubiks = [];
        for (let z in pos) {
            for (let y in pos) {
                for (let x in pos) {
                    this.Rubiks.push(this.createCube(pos[x], pos[y], pos[z]));
                }
            }
        }
    }
};

const STEP = 32;

function testVisu() {
    const canvas = document.querySelector('#cube');
    const engine = new BABYLON.Engine(canvas, true);
    let scene = createScene(canvas, engine);

    let R = new Cube(scene, STEP);

    R.move('R');

    engine.runRenderLoop(function() {
        scene.render();
     });
}

//testVisu();

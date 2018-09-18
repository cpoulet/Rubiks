main();

function main() {
    const canvas = document.querySelector('#cube');
    const engine = new BABYLON.Engine(canvas, true);
    let scene = createScene(canvas, engine);

    let Rubiks = createRubiks(scene);

    engine.runRenderLoop(function() {
        scene.render();
     });
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

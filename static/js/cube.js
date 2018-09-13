main();

var cubeRotation = 0.0;

function main() {
    const canvas = document.querySelector('#cube');
    const gl = canvas.getContext('webgl');

    // Vertex shader program

    const vsSource = `
    attribute vec4 aVertexPosition;
    attribute vec4 aVertexColor;

    uniform mat4 uModelViewMatrix;
    uniform mat4 uProjectionMatrix;

    varying lowp vec4 vColor;

    void main(void) {
      gl_Position = uProjectionMatrix * uModelViewMatrix * aVertexPosition;
      vColor = aVertexColor;
    }
  `;

    // Fragment shader program

    const fsSource = `
    varying lowp vec4 vColor;

    void main(void) {
      gl_FragColor = vColor;
    }
  `;


    // Initialize a shader program; this is where all the lighting
    // for the vertices and so forth is established.
    const shaderProgram = initShaderProgram(gl, vsSource, fsSource);

    // Collect all the info needed to use the shader program.
    // Look up which attributes our shader program is using
    // for aVertexPosition, aVevrtexColor and also
    // look up uniform locations.
    const programInfo = {
        program: shaderProgram,
        attribLocations: {
            vertexPosition: gl.getAttribLocation(shaderProgram, 'aVertexPosition'),
            vertexColor: gl.getAttribLocation(shaderProgram, 'aVertexColor'),
        },
        uniformLocations: {
            projectionMatrix: gl.getUniformLocation(shaderProgram, 'uProjectionMatrix'),
            modelViewMatrix: gl.getUniformLocation(shaderProgram, 'uModelViewMatrix'),
        },
    };

    // Here's where we call the routine that builds all the
    // objects we'll be drawing.
    const buffers = initBuffers(gl);

    var then = 0;

    // Draw the scene repeatedly
    function render(now) {
        now *= 0.001;  // convert to seconds
        const deltaTime = now - then;
        then = now;
        drawScene(gl, programInfo, buffers, deltaTime);
        requestAnimationFrame(render);
    }
    requestAnimationFrame(render);

}

function initBuffers(gl) {

    const cube = createCube();

    const positions = cube.positions;
    const positionBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(positions), gl.STATIC_DRAW);

    const colors = cube.colors;
    const colorBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(colors), gl.STATIC_DRAW);

    // Ce tableau définit chaque face comme deux triangles, en utilisant les
    // indices dans le tableau des sommets pour spécifier la position de chaque
    // triangle.

    const indices = [
        0,  1,  2,      0,  2,  3,    // avant
        4,  5,  6,      4,  6,  7,    // arrière
        8,  9,  10,     8,  10, 11,   // haut
        12, 13, 14,     12, 14, 15,   // bas
        16, 17, 18,     16, 18, 19,   // droite
        20, 21, 22,     20, 22, 23,   // gauche
    ];
    const indexBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indexBuffer);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(indices), gl.STATIC_DRAW);

    return {
        position: positionBuffer,
        color: colorBuffer,
        indices: indexBuffer,
    };
}

function drawScene(gl, programInfo, buffers, deltaTime) {
    gl.clearColor(0.0, 0.0, 0.0, 1.0);
    gl.clearDepth(1.0);                 // Clear everything
    gl.enable(gl.DEPTH_TEST);           // Enable depth testing
    gl.depthFunc(gl.LEQUAL);            // Near things obscure far things

    // Clear the canvas before we start drawing on it.

    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    // Create a perspective matrix, a special matrix that is
    // used to simulate the distortion of perspective in a camera.
    // Our field of view is 45 degrees, with a width/height
    // ratio that matches the display size of the canvas
    // and we only want to see objects between 0.1 units
    // and 100 units away from the camera.

    const fieldOfView = 45 * Math.PI / 180;   // in radians
    const aspect = gl.canvas.clientWidth / gl.canvas.clientHeight;
    const zNear = 0.1;
    const zFar = 100.0;
    const projectionMatrix = mat4.create();

    // note: glmatrix.js always has the first argument
    // as the destination to receive the result.
    mat4.perspective(projectionMatrix,
        fieldOfView,
        aspect,
        zNear,
        zFar);

    // Set the drawing position to the "identity" point, which is
    // the center of the scene.
    const modelViewMatrix = mat4.create();


    // Translation
    mat4.translate(
        modelViewMatrix,
        modelViewMatrix,
        [-0.0, 0.0, -6.0]);
    // Rotation
    mat4.rotate(
        modelViewMatrix,
        modelViewMatrix,
        cubeRotation,
        [0, 0, 1]);
    mat4.rotate(
        modelViewMatrix,
        modelViewMatrix,
        cubeRotation * 0.7,
        [0, 1, 0]);


    // Tell WebGL how to pull out the positions from the position
    // buffer into the vertexPosition attribute
    {
        const numComponents = 3;
        const type = gl.FLOAT;
        const normalize = false;
        const stride = 0;
        const offset = 0;
        gl.bindBuffer(gl.ARRAY_BUFFER, buffers.position);
        gl.vertexAttribPointer(
            programInfo.attribLocations.vertexPosition,
            numComponents,
            type,
            normalize,
            stride,
            offset);
        gl.enableVertexAttribArray(
            programInfo.attribLocations.vertexPosition);
    }

    // Tell WebGL how to pull out the colors from the color buffer
    // into the vertexColor attribute.
    {
        const numComponents = 4;
        const type = gl.FLOAT;
        const normalize = false;
        const stride = 0;
        const offset = 0;
        gl.bindBuffer(gl.ARRAY_BUFFER, buffers.color);
        gl.vertexAttribPointer(
            programInfo.attribLocations.vertexColor,
            numComponents,
            type,
            normalize,
            stride,
            offset);
        gl.enableVertexAttribArray(
            programInfo.attribLocations.vertexColor);
    }

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, buffers.indices);

    // Tell WebGL to use our program when drawing

    gl.useProgram(programInfo.program);

    // Set the shader uniforms

    gl.uniformMatrix4fv(
        programInfo.uniformLocations.projectionMatrix,
        false,
        projectionMatrix);
    gl.uniformMatrix4fv(
        programInfo.uniformLocations.modelViewMatrix,
        false,
        modelViewMatrix);

    {
        const vertexCount = 36;
        const type = gl.UNSIGNED_SHORT;
        const offset = 0;
        gl.drawElements(gl.TRIANGLES, vertexCount, type, offset);
    }

    {
        const offset = 0;
        const vertexCount = 4;
        gl.drawArrays(gl.TRIANGLE_STRIP, offset, vertexCount);
    }
    cubeRotation += deltaTime;
}

function initShaderProgram(gl, vsSource, fsSource) {
    const vertexShader = loadShader(gl, gl.VERTEX_SHADER, vsSource);
    const fragmentShader = loadShader(gl, gl.FRAGMENT_SHADER, fsSource);

    // Create the shader program

    const shaderProgram = gl.createProgram();
    gl.attachShader(shaderProgram, vertexShader);
    gl.attachShader(shaderProgram, fragmentShader);
    gl.linkProgram(shaderProgram);

    if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) {
        alert('Unable to initialize the shader program: ' + gl.getProgramInfoLog(shaderProgram));
        return null;
    }

    return shaderProgram;
}

function loadShader(gl, type, source) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);

    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        alert('An error occurred compiling the shaders: ' + gl.getShaderInfoLog(shader));
        gl.deleteShader(shader);
        return null;
    }
    return shader;
}

function createCube(size, x, y, z) {

    size = size ? size : 1.0;
    x = x ? x : 0.0;
    y = y ? y : 0.0;
    z = z ? z : 0.0;

    const positions = [
    // Face avant
    -size + x, -size + y,  size + z,
     size + x, -size + y,  size + z,
     size + x,  size + y,  size + z,
    -size + x,  size + y,  size + z,

    // Face arrière
    -size + x, -size + y, -size + z,
    -size + x,  size + y, -size + z,
     size + x,  size + y, -size + z,
     size + x, -size + y, -size + z,

    // Face supérieure
    -size + x,  size + y, -size + z,
    -size + x,  size + y,  size + z,
     size + x,  size + y,  size + z,
     size + x,  size + y, -size + z,

    // Face inférieure
    -size + x, -size + y, -size + z,
     size + x, -size + y, -size + z,
     size + x, -size + y,  size + z,
    -size + x, -size + y,  size + z,

    // Face droite
     size + x, -size + y, -size + z,
     size + x,  size + y, -size + z,
     size + x,  size + y,  size + z,
     size + x, -size + y,  size + z,

    // Face gauche
    -size + x, -size + y, -size + z,
    -size + x, -size + y,  size + z,
    -size + x,  size + y,  size + z,
    -size + x,  size + y, -size + z
  ];

    const faceColors = [
    [1.0,  0.5,  0.0,  1.0],    // Face avant : orange
    [1.0,  0.0,  0.0,  1.0],    // Face arrière : rouge
    [0.0,  0.0,  1.0,  1.0],    // Face supérieure : bleu
    [0.0,  1.0,  0.0,  1.0],    // Face infiérieure : vert
    [1.0,  1.0,  1.0,  1.0],    // Face droite : blanc
    [1.0,  1.0,  0.0,  1.0]     // Face gauche : jaune
  ];

  // Conversion du tableau des couleurs en une table pour tous les sommets

  var colors = [];

  for (j=0; j<faceColors.length; j++) {
    const c = faceColors[j];

    // Répéter chaque couleur quatre fois pour les quatre sommets d'une face
    colors = colors.concat(c, c, c, c);
  }

    return {
        positions: positions,
        colors: colors,
    };
}

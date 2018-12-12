export class Archi {
    constructor() {
        this.newCube();
    }

    newCube() {
        this.archi = [];
        for (let i = 0; i < 27; i++) {
            this.archi.push(i);
        }
    }

    updateArchi(move, dir) {
        if (dir == 1) {
            this['rot' + move]();
        } else {
            for (let i = 0; i < 3; i++) {
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
};

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

//testArchi();

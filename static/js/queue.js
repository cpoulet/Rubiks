export class Queue {
    constructor() {
        this.queue = [];
    }

    push(m, foo=null) {
        this.queue.unshift(m);
        if (foo !== null) {
            foo(m);
        }
    }

    pop() {
        let x = this.queue.pop();
        return x === undefined ? false : x;
    }

    show() {
        console.log(this.queue);
    }

    empty() {
        return this.size() == 0;
    }

    size() {
        return this.queue.length;
    }
    
    reset() {
        this.queue = [];
    }
};

function testQueue() {
    q = new Queue;

    q.empty();


}

//testQueue();

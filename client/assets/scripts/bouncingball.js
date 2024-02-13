console.log("Running bouncing ball")

const count_display = document.querySelector("p")
let count = 0;
const canvas = document.querySelector("canvas");
const ctx = canvas.getContext('2d');

const width = (canvas.width = window.innerWidth)
const height = (canvas.height = window.innerHeight)

function random(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }
  
  function randomRGB() {
    return `rgb(${random(0, 255)} ${random(0, 255)} ${random(0, 255)})`;
  }

class Shape{
    constructor(x,y,vel_x,vel_y){
        this.x = x;
        this.y = y;
        this.vel_x= vel_x;
        this.vel_y = vel_y;
    }
}
class Ball extends Shape{
    constructor(x, y, vel_x, vel_y,size,color){
        super(x,y,vel_x,vel_y);
        this.size = size;
        this.color = color;
        this.exists = true;
    }

    draw(){
        ctx.beginPath()
        ctx.fillStyle = this.color;
        ctx.arc(this.x,this.y,this.size, 0, 2*Math.PI)
        ctx.fill()
    }

    update(){
        if( (this.x + this.vel_x) >= width){
            this.vel_x = -this.vel_x;
        }
        if ((this.x + this.vel_x) <= 0){
            this.vel_x = -this.vel_x;
        }
        if ((this.y + this.vel_y) >= height){
            this.vel_y = -this.vel_y;
        }
        if ((this.y + this.vel_y) <= 0){
            this.vel_y = -this.vel_y;
        }

        this.x += this.vel_x;
        this.y += this.vel_y;
    }

    collision_detect(){

        for (const ball of balls){
            if (!(this===ball) && ball.exists){
                const dx = this.x - ball.x;
                const dy = this.y - ball.y;
                const dist = Math.sqrt(dx*dx + dy*dy);

                if (dist < (this.size + ball.size)){
                    ball.color = this.color = randomRGB()
                }

            }
        }
    }
}

class Evil_Ball extends Shape{
    constructor(x,y){
        super(x,y,20,20);
        this.color = 'white';
        this.size = 10;

        window.addEventListener('keydown', (e)=>{
            switch(e.key){
                case 'a':
                    this.x -= this.vel_x;
                    break;
                case 'd':
                    this.x += this.vel_x;
                    break;
                case 'w':
                    this.y -=  this.vel_y;
                    break;
                case 's':
                    this.y += this.vel_y;
                    break;
            }
        });
    }

    check_bounds(){
        if( (this.x + this.vel_x) >= width){
            this.x -= this.size;
        }
        if ((this.x + this.vel_x) <= 0){
            this.x += this.size;
        }
        if ((this.y + this.vel_y) >= height){
            this.y -= this.size;
        }
        if ((this.y + this.vel_y) <= 0){
            this.y += this.size;
        }
    }

    draw(){
        ctx.beginPath();
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 3;
        ctx.arc(this.x, this.y, this.size,0, 2*Math.PI)
        ctx.stroke()
    }

    collision_detect(){

        for (const ball of balls){
            if (ball.exists){
                const dx = this.x - ball.x;
                const dy = this.y - ball.y;
                const dist = Math.sqrt(dx*dx + dy*dy);

                if (dist < (this.size + ball.size)){
                    ball.exists = false;
                    count--;
                    count_display.textContent = `Ball Count: ${count}`

                }

            }
        }

    }


    
   
}

let balls = [];

while(balls.length < 25){

    const size = random(10,20);
    
    const ball = new Ball(
        random(size, width-size),
        random(size, height-size),
        random(-7,-7),
        random(-7,7),
        size,
        randomRGB()
    )
    balls.push(ball)
    count++;
    count_display.textContent = `Ball Count: ${count}`

}

const evil_ball = new Evil_Ball(random(0,width), random(0,height))

function create_animation(){

    ctx.fillStyle = "rgb(0 0 0 / 25%)";
    ctx.fillRect(0,0,width,height);

    for (const ball of balls){
        if (ball.exists){
            ball.draw();
            ball.update();
            ball.collision_detect()
        }
    }

    evil_ball.draw();
    evil_ball.check_bounds();
    evil_ball.collision_detect();

    requestAnimationFrame(create_animation);

}

create_animation();
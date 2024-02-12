
let row_size = 25;
let col_size = 40;
let grid_size= '5px'
let matrix = [];
let is_playing = false;
let interval_id;

const start_button = document.querySelector('.start');
const reset_button = document.querySelector('.reset');
const random_button = document.querySelector('.random')
const game_grid = document.querySelector('.gamegrid');

function create_board(rows=row_size,cols= col_size){
    console.log("Generating board");
    for (let r = 0; r < rows; r++) {
        
        let row_div = document.createElement('div')
        row_div.className = 'gridrow'

        let row = [];
        for(let c = 0; c < cols; c++ ){
            col_val = 0;
            row[c] = col_val;
              
            let cell = document.createElement('div')
            cell.className = 'cell'
            cell.id = `${r}-${c}`
           
            cell.textContent = col_val
            cell.style.backgroundColor = 'white'
            row_div.appendChild(cell)


        }
        //console.log(`Row no: ${r} and value: ${row}`);
        matrix[r] = row;
        game_grid.appendChild(row_div)
        

    }
    
    console.log(matrix);
}


function update_board(){
    console.log("Updating grid...")
    for(let r=0; r<row_size;r ++){
        for (let c=0; c<col_size;c++){
            cell_id =`${r}-${c}`
            let cell = document.getElementById(cell_id);
            // console.log(`${cell_id}   :  ${matrix[r][c]}`)
            cell.textContent = matrix[r][c];
            cell.style.backgroundColor = (matrix[r][c] === 1) ? 'green' : 'white'

        }
    }
}

function get_next_gen(){
    console.log("Getting next gen")
}

function start_game(){
    if (is_playing){
        interval_id = setInterval(get_next_gen, 1000)
    }

}


function refill_board(how){
    
    console.log(`Refelling board : ${how}`)
    for (let r=0; r<row_size; r++){
        let row=[];
        for (let c=0; c<col_size; c++){
            val = (how==='reset') ? 0 : Math.round(Math.random())
            row[c] = val;
        }
        matrix[r] = row;
    }

    update_board();
    console.log(matrix);
   
}

function get_user_click(){
    
    cell_idl = this.id.split("-")
    row_id = Number(cell_idl[0]);
    col_id = Number(cell_idl[1]);

    console.log("got user click in the grid")
    console.log(this.id)
    console.log(`${row_id} * ${col_id} : ${matrix[row_id][col_id]}`)
    
    matrix[row_id][col_id] = (matrix[row_id][col_id] === 1) ? 0:1;
    console.log(`Changed to:  ${matrix[row_id][col_id]}`)

    this.textContent = matrix[row_id][col_id]
    this.style.backgroundColor = (matrix[row_id][col_id] === 1) ? 'green' : 'white'

}



console.log("running Game of Life")

// This needs to run first before adding listener to each cell. 
create_board()

// Adding listener to the button
start_button.addEventListener('click',()=>{

    console.log(`present isplaying: ${is_playing}`)
    console.log(`the button text is : ${start_button.textContent}`)

    if (is_playing){
        console.log("is playing is true")
        is_playing = false
        start_button.textContent = 'Start'
        clearInterval(interval_id)
    }else{
        console.log("is playing is false")
        start_button.textContent = 'Stop'
        is_playing = true
        start_game()
    }    

})

reset_button.addEventListener('click',()=>{
    refill_board('reset')
})
random_button.addEventListener('click',()=>{
    refill_board('random')
})

// Adding click listener to each cells
all_cell = document.querySelectorAll('.cell')
for (const c of all_cell){
    c.addEventListener('click', get_user_click);
}




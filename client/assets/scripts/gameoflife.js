
// grid and matrix variable
let row_size =75;
let col_size = 150;

const color_map = {
    0: 'grey',
    1: 'yellow',
    
}
// 2D Matrix representation of the board 
let matrix = []; 
let neighbour_matrix = []

// start game variables
let is_playing = false;
let interval_id;



const start_button = document.querySelector('.start');
const next_button = document.querySelector('.next');

const reset_button = document.querySelector('.reset');
const random_button = document.querySelector('.random')
const game_grid = document.querySelector('.gamegrid');

// tracks if the user clicked on game grid and updates the matrix and grid
function track_user_click(){
    cell_idl = this.id.split("-")
    row_id = Number(cell_idl[0]);
    col_id = Number(cell_idl[1]);
    matrix[row_id][col_id] = (matrix[row_id][col_id] === 1) ? 0:1;
    
    // update neighbour

    // this.textContent = matrix[row_id][col_id]
    this.style.backgroundColor = color_map[matrix[row_id][col_id]]
}

function setup_grids(rows = row_size, cols = col_size){
    
    
    for (let r = 0; r < rows; r++) {
        
        let row_div = document.createElement('div')
        row_div.className = 'gridrow'
        for(let c = 0; c < cols; c++ ){
            let cell = document.createElement('div')
            cell.className = 'cell'
            cell.id = `${r}-${c}`
           
            // cell.textContent = neighbour_matrix[r][c]
            cell.style.backgroundColor = color_map[0]
            // adding listerner to each clicks
            cell.addEventListener('click', track_user_click)
            row_div.appendChild(cell)


        }
        game_grid.appendChild(row_div)   
    }
    

}

function init_gameoflife(){
    refill_matrix("reset", false)
    setup_grids()
   
}

function update_board(){
    
    for(let r=0; r<row_size;r ++){
        for (let c=0; c<col_size;c++){
            cell_id =`${r}-${c}`
            let cell = document.getElementById(cell_id);
            // cell.textContent = neighbour_matrix[r][c];
            cell.style.backgroundColor = color_map[matrix[r][c]] 

        }
    }
}

function refill_matrix(how="reset", update_grids = true){
    let new_matrix = []
    
    for (let r=0; r<row_size; r++){
        let row=[];
        for (let c=0; c<col_size; c++){
            let val = 0 ; 
            if (how === 'random') {
                val = Math.round(Math.random());
            } else if (how === 'nextgeneration') {
                val = next_generation(r,c)

            }
            row[c] = val;
        }
        new_matrix[r] = row;
    }
    matrix = new_matrix;
    calculate_neighbour_matrix()
    if (update_grids){
        update_board()
    }
        
   
}

function get_neighbour(row,col){
    let neigh = []
    if (row > 0 ){
       neigh.push(matrix[row-1][col])
    }
    if (col > 0 ){
        neigh.push(matrix[row][col-1])
    }

    if (row > 0 && col > 0 ){
        neigh.push(matrix[row-1][col-1])
    }



    if (row < row_size -1 ){
        neigh.push(matrix[row+1][col])
    }
    if (col < col_size -1 ){
        neigh.push(matrix[row][col+1])
    }
    if (row < row_size -1  && col < col_size -1  ){
        neigh.push(matrix[row+1][col+1])
    }

    if (row > 0 && col<col_size -1){
        neigh.push(matrix[row-1][col+1])
    }
    if (row <row_size-1 && col> 0 ){
        neigh.push(matrix[row+1][col-1])
    }
    return neigh


}

function calculate_neighbour_matrix(){
    for (let r=0; r < row_size; r++){
        let row = [];
        for(let c=0; c < col_size; c++){
            neighbor_vals = get_neighbour(r,c)
            row[c] = neighbor_vals.reduce((acc,v) => acc + v, 0);
        }
        neighbour_matrix[r] = row
    }
}

function next_generation(row,col){
    // if cell is alive:
    //     cell with one or no neighbour dies of soltitude
    //     cell with four or more neighbour dies of overpopulation
    //     cell with cell with two or three neighour survives

    // if cell is empty:
    // cell with three neighbour becomes populates
    all_neighbour = get_neighbour(row,col)
    total_neighbour = all_neighbour.reduce((acc,v) => acc + v, 0);
    
    val = matrix[row][col]
    result = 0;

    if(val===0){
       if (total_neighbour===3){
           result = 1;
       }
    }else{
        if (total_neighbour <=1 ) {
            result = 0;
        } else if(total_neighbour >=4){
            result = 0;
        }else{
            result = 1;
        }

    }
    return result


}

function start_game(){
    if (is_playing){
        interval_id = setInterval(()=>{
           
            refill_matrix('nextgeneration')
            calculate_neighbour_matrix()
    
        }, Math.round(1000/30))
    }

}







console.log("running Game of Life")

// This needs to run first before adding listener to each cell. 
init_gameoflife()

// Adding listener to the button
start_button.addEventListener('click',()=>{

  
    if (is_playing){
        is_playing = false
        start_button.textContent = 'Start'
        clearInterval(interval_id)
    }else{
    
        start_button.textContent = 'Stop'
        is_playing = true
        start_game()
    }    

})


next_button.addEventListener('click',()=>{
    
    refill_matrix('nextgeneration')
    
    
})

reset_button.addEventListener('click',()=>{
    refill_matrix('reset')

})
random_button.addEventListener('click',()=>{
    refill_matrix('random')
    
})






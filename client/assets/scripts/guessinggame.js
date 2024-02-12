
let user_guess;
const total_attempt = 10;
let user_attempt = 1
let game_number = Math.floor(Math.random() * 100 ) + 1;

const user_submit_button = document.querySelector('.userSubmit');
const user_input = document.querySelector('.userGuess');

const guessHistory = document.querySelector('.guessHistory')
const highLowText = document.querySelector('.highLow')
const gameStatus = document.querySelector('.gameStatus')

let resetButton;

function resetGame(){
  
  highLowText.textContent="";
  user_input.disabled = true;
  user_submit_button.disabled= true;
  
  resetButton = document.createElement('button');
  resetButton.textContent = "Play Again"
  document.body.append(resetButton);
  resetButton.addEventListener('click', setDefaultValues);

}

function setDefaultValues(){

  game_number = Math.floor(Math.random() * 100 ) + 1;
  user_guess = 0;
  user_attempt = 1;

  user_input.disabled = false;
  user_input.value="";
  user_submit_button.disabled = false;
  
  guessHistory.textContent = "";
  gameStatus.textContent=""

  resetButton.parentNode.removeChild(resetButton)
  user_input.focus();


}

function checkGuess(){
  user_guess = Number(user_input.value);

  if (user_attempt === 1 ){
    guessHistory.textContent = "Guess history: ";
  }

  guessHistory.textContent = `${guessHistory.textContent} ${user_guess}`
  if (user_guess === game_number) {
    console.log("Correct Guess ");
    gameStatus.textContent = "You Win";
    gameStatus.style.backgroundColor = 'green';
    resetGame()
    
  } else if(user_attempt === total_attempt){
    console.log("Game over");
    gameStatus.textContent = "Game Over";
    gameStatus.style.backgroundColor = 'red';
    resetGame()
  
  } else {
    console.log("Incorrect guess")
    gameStatus.textContent = "Incorrect Guess";
    gameStatus.style.backgroundColor = 'orange';
    
    if (user_guess < game_number) {
      highLowText.textContent = "Last guess was Low";
       
    } else {
      highLowText.textContent = "Last guess was High";
    }
    user_attempt += 1;
    user_input.value="";
    user_input.focus();


  }

   
}

user_submit_button.addEventListener('click', checkGuess)
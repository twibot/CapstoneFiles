const container = document.querySelector('.container');
// const parkingSpots = document.querySelectorAll('.row .parking_spots:not(.occupied)')
const parkingSpots = document.querySelector('.parking_spots');

const button = document.querySelector('#pushbutton');

//Function takes the container class and add an "click" event. Upon clicking a parking spot, it will be highlighted blue due to the
//due to the naming of it changing it to parking_spots Selected
container.addEventListener('click', e => {
  if( e.target.classList.contains('parking_spots') && !e.target.classList.contains('occupied') )
  {
    e.target.classList.toggle('selected');

  }
});

button.addEventListener('click', e => {
  console.log("outside");
  if( parkingSpots.classList.contains('parking_spots') && parkingSpots.classList.contains('selected') )
  { 
    console.log("inside");
    e.classList.remove('selected');
    e.classList.add('reserved');
    
  }
});


//add ID to every parking spot, Loop from 1-x, use the index, const temp = ps+index, if ps.index contains above if statement than 
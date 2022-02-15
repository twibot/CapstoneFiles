const container = document.querySelector('.container');
const parkingSpots = document.querySelectorAll('.row .parking_spots:not(.occupied)')


container.addEventListener('click', e => {
  if( e.target.classList.contains('parking_spots') && !e.target.classList.contains('occupied') )
  {
    e.target.classList.toggle('selected')
  }
  
})
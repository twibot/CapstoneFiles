const container = document.querySelector('.container');
const parkingSpots = document.querySelector('.parking_spots');
const button = document.querySelector('#pushbutton');
const count = document.getElementById('count');
var tmp;

//Function takes the container class and add an "click" event. Upon clicking a parking spot, it will be highlighted blue due to the
//due to the naming of it changing it to parking_spots Selected
container.addEventListener('click', e => {
  if( e.target.classList.contains('parking_spots') && !e.target.classList.contains('occupied') )
  {
    e.target.classList.toggle('selected');
    tmp = e.target;
  }
});


button.addEventListener('click', e => {
  if(tmp.classList.contains('parking_spots') && tmp.classList.contains('selected'))
  {
    tmp.classList.remove('selected');
    tmp.classList.add('reserved');
  }
});

function countingstars() {
  document.getElementById("output").innerHTML = ++count;
}

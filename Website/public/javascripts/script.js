const container = document.querySelector('.container');
const parkingSpots = document.querySelectorAll('.parking_slot');
const button = document.querySelector('#pushbutton');
const count = document.getElementById('count');
var tmp;
var slot_selector;
//Function takes the container class and add an "click" event. Upon clicking a parking spot, it will be highlighted blue due to the
//due to the naming of it changing it to parking_spots Selected

 for(var i =0; i < parkingSpots.length; i++){
	 parkingSpots[i].addEventListener('click', e => {
		if( e.target.classList.contains('parking_slot') && !e.target.classList.contains('occupied') )
		{
			e.target.classList.toggle('selected');
			slot_selector = e.target;
			tmp = e.target.id;
		}
	})
	 
 }

button.addEventListener('click', e => {
  if(slot_selector.classList.contains('parking_slot') && slot_selector.classList.contains('selected'))
  {
	
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", "//localhost:3000/update?psid=" + tmp, true);

	xhttp.send();
	xhttp.onreadystatechange = function() {
		slot_selector.classList.remove('selected');
		slot_selector.classList.add('reserved');
    }

  }
})

function countingstars() {
  document.getElementById("output").innerHTML = ++count;
}



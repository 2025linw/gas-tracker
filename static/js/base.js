'use strict';

// Select vehicle
function selectVehicle(vehicle) {
  const currentVehicleSpan = document.getElementById('current-vehicle');
  currentVehicleSpan.innerHTML = '';
  currentVehicleSpan.dataset.vehicleId = vehicle.id.slice(8);

  const clone = vehicle.cloneNode(true);
  for (const e of Array.from(clone.childNodes)) {
    currentVehicleSpan.appendChild(e);
  }
}

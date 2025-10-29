async function submitReceipt() {
  const apiUrl = '/api/receipts';

  const vehicleId = document.getElementById('current-vehicle').dataset.vehicleId;
  if (!vehicleId) {
    console.error("No vehicle has been selected");

    return;
  }

  const stationId = parseInt(document.getElementById('station-select').value);
  if (isNaN(stationId)) {
    console.error("Invalid gas station ID selected");

    return;
  }
  const gallons = parseFloat(document.getElementById('gallon-input').value);
  if (isNaN(gallons)) {
    console.error("Invalid gallon amount entered");

    return;
  }
  const pricePerGallon = parseFloat(document.getElementById('ppg-input').value);
  if (isNaN(pricePerGallon)) {
    console.error("Invalid price per gallon amount entered");

    return;
  }

  console.log({
    vehicleId,
    stationId,
    gallons,
    pricePerGallon,
  });

  const res = await fetch(apiUrl, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      vehicleId,
      stationId,
      gallons,
      pricePerGallon,
    }),
  });
  // const gallons =
  // console.log(station.value);
}

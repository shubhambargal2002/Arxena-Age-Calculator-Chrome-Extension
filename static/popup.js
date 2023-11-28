// console.log('Popup.js loaded');

document.addEventListener('DOMContentLoaded', function () {
  // Fetch and populate dropdown with profiles
  fetch('http://localhost:5000/profiles')
    .then(response => response.json())
    .then(profiles => {
      const selector = document.getElementById('profileSelector');
      profiles.forEach(profile => {
        const option = document.createElement('option');
        option.value = profile.name;
        option.text = profile.name;
        selector.add(option);
      });
    })
    .catch(error => console.error('Error fetching profiles:', error));

  // Add event listener for dropdown change
  document.getElementById('profileSelector').addEventListener('change', function () {
    const selectedProfile = this.value;

    // console.log('Selected Profile:', selectedProfile);

    // Fetch approximate age and display
    fetch(`http://localhost:5000/age?name=${selectedProfile}`)
      .then(response => response.json())
      .then(data => {
        // console.log('Fetched age data:', data); // Add this line to log the received data
        document.getElementById('ageDisplay').innerText = `Approximate Age: ${data.age}`;
      })
      .catch(error => console.error('Error fetching age:', error));
  });
});

<template>
  <div>
    <div class="container mt-5">
      <div class="row row-cols-1 row-cols-md-4 g-4">
        <div v-for="venue in venues_data" :key="venue.vid" class="col">
          <div class="card">
            <img
              :src="require('@/assets/mad2image.png')"  
              class="card-img-top"
            >
            <div class="card-body">
              <h5 class="card-title">{{ venue.venue }}</h5>
              <h6 class="card-subtitle mb-2 text-muted">{{ venue.loc }}</h6>
              <h6 class="card-text">{{ venue.cap }}</h6>
  
              <button @click="editvenue(venue.vid)" class="btn btn-primary">Edit</button>
  
              <button @click="deletevenue(venue.vid)" class="btn btn-danger">Delete</button>
              <button @click="goToashows(venue.vid)" class="btn btn-success">Show</button>
              <button @click="exportt(venue.vid)" class="btn btn-info">Export</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  
    <div class="text-center mt-3">
      <button @click="goToVenueform" class="btn btn-primary">Add Venue</button>
    </div>
  </div>
</template>
  
  <script>
  export default {
    data() {
      return {
        venues_data: [],
        access_token: null,
        username: null,
      };
    },
    methods: {
      editvenue(vid) {
        this.$router.push('/venueformedit/' + vid);
      },
      exportt(vid) {
        window.location.href = `http://127.0.0.1:5000/download_csv?vid=${vid}`;
      },
      goToVenueform() {
        this.$router.push('/venueform');
      },
      goToashows(vid) {
        this.$router.push('/showpage/' + vid);
      },
      deletevenue(vid3) {
        const confirmation = window.confirm("Are you sure you want to delete this show?");
        if (confirmation) {
        fetch(`http://127.0.0.1:5000/api/venuedelete/${vid3}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          },
        })
          .then((response) => {
            if (response.ok) {
              this.$router.push('/advenue'); // Navigate to the "venue" page
            } else {
              // Handle the response when there's an error (optional)
              console.error('Venue creation failed');
            }
          })
          .catch((error) => {
            // Handle any network errors (optional)
            console.error('Network error:', error);
          });
      }},
    },
    created() {
      this.access_token = localStorage.getItem('access_token');
      if (!this.access_token) {
        console.error('Access Token not found in localStorage.');
        // Handle the case where the token is missing
        return;
      }
  
      console.log('Access Token:', this.access_token);
  
      fetch('http://127.0.0.1:5000/api/venueget', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + this.access_token, // Include the access token in the headers
        },
      })
        .then((response) => response.json()) // Parse the JSON data from the response
        .then((data) => {
          console.log('Response data:', data);
          this.venues_data = data; // Update the venues_data with the fetched data
        })
        .catch((error) => {
          console.error('Error fetching venues:', error);
        });
    },
  };
  </script>
  
<template>
  <div>
    <!-- Search input field -->
    <input type="text" v-model="searchQuery" @input="searchVenues" placeholder="Search venues">

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
              <button type="submit" @click="goToUshows(venue.vid)" class="btn btn-success">Show</button>
            </div>
          </div>
        </div>
      </div>
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
      searchQuery: '', // The search query entered by the user
      allVenues: [], // A copy of all venues for filtering
    };
  },
  methods: {
    goToUshows(vid) {
      this.$router.push('/ushows/' + vid);
    },

    searchVenues() {
      const searchQuery = this.searchQuery.trim().toLowerCase();
      if (!searchQuery) {
        // If the search query is empty, show all venues
        this.venues_data = this.allVenues;
        return;
      }

      this.venues_data = this.allVenues.filter(venue => {
        // Customize the condition for your search
        // Here, we are searching by venue name and location
        const venueName = venue.venue.toLowerCase();
        const location = venue.loc.toLowerCase();
        return venueName.includes(searchQuery) || location.includes(searchQuery);
      });
    },
  },

  created() {
    this.access_token = localStorage.getItem("access_token");
    if (!this.access_token) {
      console.error("Access Token not found in localStorage.");
      // Handle the case where the token is missing
      return;
    }

    fetch('http://127.0.0.1:5000/api/venueget', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + this.access_token // Include the access token in the headers
      }
    })
    .then(response => response.json())
    .then(data => {
      console.log("Response data:", data);
      this.venues_data = data;
      // Keep a copy of all venues in a separate variable for filtering
      this.allVenues = data;
    })
    .catch(error => {
      console.error("Error fetching venues:", error);
    });
  },
};
</script>


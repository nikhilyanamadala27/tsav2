<template>
  <div>
    <!-- Search input field -->
    <input type="text" v-model="searchQuery" @input="searchShows" placeholder="Search shows" class="form-control mb-3">

    <div class="container mt-5">
      <div class="row row-cols-1 row-cols-md-4 g-4">
        <div class="col" v-for="show in filteredShows" :key="show.sid">
          <div class="card">
            <img
              :src="require('@/assets/mad2image.png')"  
              class="card-img-top"
            >
            <div class="card-body">
              <h5 class="card-title">{{ show.showname }}</h5>
              <h6 class="card-subtitle mb-2 text-muted">{{ show.genre }}</h6>
              <h6 class="card-text">{{ show.bookings }}</h6>
              <button @click="goToBook(show.sid)" class="btn btn-success">Book</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
  <script>
  export default {
    props: ['vid'],
    data() {
      return {
        showget: [],
        access_token: null,
        username: null,
        searchQuery: '', // The search query entered by the user
        allShows: [], // A copy of all shows for filtering
      };
    },
    computed: {
      filteredShows() {
        const searchQuery = this.searchQuery.trim().toLowerCase();
        if (!searchQuery) {
          // If the search query is empty, show all shows
          return this.showget;
        }
  
        return this.showget.filter(show => {
          // Customize the condition for your search
          // Here, we are searching by show name and genre
          const showName = show.showname.toLowerCase();
          const genre = show.genre.toLowerCase();
          return showName.includes(searchQuery) || genre.includes(searchQuery);
        });
      },
    },
    methods: {
      goToBook(sid) {
        this.$router.push('/book/' + sid);
      },
  
      searchShows() {
        const searchQuery = this.searchQuery.trim().toLowerCase();
        if (!searchQuery) {
          // If the search query is empty, show all shows
          this.showget = this.allShows;
          return;
        }
  
        this.showget = this.allShows.filter(show => {
          // Customize the condition for your search
          // Here, we are searching by show name and genre
          const showName = show.showname.toLowerCase();
          const genre = show.genre.toLowerCase();
          return showName.includes(searchQuery) || genre.includes(searchQuery);
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
  
      const vid = this.$route.params.vid;
  
      fetch(`http://127.0.0.1:5000/api/showget/${vid}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + this.access_token // Include the access token in the headers
        }
      })
      .then(response => response.json())
      .then(data => {
        console.log("Response data:", data);
        this.showget = data;
        // Keep a copy of all shows in a separate variable for filtering
        this.allShows = data;
      })
      .catch(error => {
        console.error("Error fetching shows:", error);
      });
    },
  };
  </script>
  
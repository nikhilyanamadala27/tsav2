<template>
  <div>
    <div class="text-center mb-3">
      <button @click="addshow" class="btn btn-primary">Add Show</button>
    </div>
    <div class="container mt-5">
      <div class="row row-cols-1 row-cols-md-4 g-4">
        <div class="col" v-for="show in showget" :key="show.sid">
          <div class="card">
            <img
              :src="require('@/assets/mad2image.png')"  
              class="card-img-top"
            >
            <div class="card-body">
              <h5 class="card-title">{{ show.showname }}</h5>
              <h6 class="card-subtitle mb-2 text-muted">{{ show.genre }}</h6>
              <h6 class="card-text">{{ show.bookings }}</h6>
              <button @click="editshow(show.sid)" class="btn btn-primary">Edit</button>
              <button @click="deleteshow(show.sid)" class="btn btn-danger">Delete</button>
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
    };
  },
  methods: {
    addshow() {
      const vid = this.$route.params.vid;
      this.$router.push('/showform/' + vid);
    },
    editshow(sid) {
      this.$router.push('/showeform/' + sid);
    },
    deleteshow(sid) {
      const confirmation = window.confirm("Are you sure you want to delete this show?");
      if (confirmation) {
        fetch(`http://127.0.0.1:5000/api/showdelete/${sid}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          },
        })
        .then((response) => {
          if (response.ok) {
            this.$router.push('/advenue'); // Navigate to the "venue" page
          } else {
            console.error('Show deletion failed');
          }
        })
        .catch((error) => {
          console.error('Network error:', error);
        });
      }
    },
  },
  
  created() {
    this.access_token = localStorage.getItem('access_token');
    if (!this.access_token) {
      console.error('Access Token not found in localStorage.');
      // Handle the case where the token is missing
      return;
    }
  
    const vid = this.$route.params.vid;
  
    fetch(`http://127.0.0.1:5000/api/showget/${vid}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + this.access_token, // Include the access token in the headers
      },
    })
    .then((response) => response.json()) // Parse the JSON data from the response
    .then((data) => {
      console.log('Response data:', data);
      this.showget = data; // Update the showget with the fetched data
    })
    .catch((error) => {
      console.error('Error fetching shows:', error);
    });
  },
};
</script>


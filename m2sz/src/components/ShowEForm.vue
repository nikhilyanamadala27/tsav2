<template>
    <div>
      <div class="mb-3">
        <label class="form-label">showname</label>
        <input type="text" class="form-control" v-model="showname" name="sowname">
        <div id="emailHelp" class="form-text">We'll never share your details with anyone else.</div>
      </div>
      <div class="mb-3">
        <label class="form-label">genre</label>
        <input type="text" class="form-control" v-model="genre" name="genre">
      </div>
      <div class="mb-3">
        <label class="form-label">bookings</label>
        <input type="text" class="form-control" v-model="bookings" name="bookings">
      </div>
      <button type="submit" class="btn btn-primary" @click="goTousshowforms">submit</button>
    </div>
  </template>
  
  <script>
  export default {
    props: ['sid'],
    data() {
      return {
        showname: '',
        genre: '',
        bookings: ''
      };
    },
    methods: {
      goTousshowforms() {
        const data = {
          showname: this.showname,
          genre: this.genre,
          bookings: this.bookings
        };
        // Use the correct 'sid' prop from the component's props
        const sid4 = this.$route.params.sid;
        fetch(`http://127.0.0.1:5000/api/showput/${sid4}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        }).then(response => {
          if (response.ok) {
            this.$router.push('/advenue'); // Navigate to the "venue" page
          } else {
            // Handle the response when there's an error (optional)
            console.error('Show update failed');
          }
        }).catch(error => {
          // Handle any network errors (optional)
          console.error('Network error:', error);
        });
      }
    }
  };
  </script>
  
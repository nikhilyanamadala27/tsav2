<template>
    <div>
      <div class="mb-3">
        <label class="form-label">venue</label>
        <input type="text" class="form-control" v-model="venue" name="venue">
        <div id="emailHelp" class="form-text">We'll never share your details with anyone else.</div>
      </div>
      <div class="mb-3">
        <label class="form-label">location</label>
        <input type="text" class="form-control" v-model="loc" name="loc">
      </div>
      <div class="mb-3">
        <label class="form-label">capacity</label>
        <input type="text" class="form-control" v-model="cap" name="cap">
      </div>
      <button type="submit" class="btn btn-primary" @click="goTousVenuefrom">submit</button>
    </div>
  </template>
  
  <script>
  export default {
    props: ['vid'],
    data() {
      return {
        venue: '',
        cap: '',
        loc: ''
      };
    },
    methods: {
      goTousVenuefrom() {
        const data = {
          venue: this.venue,
          cap: this.cap,
          loc: this.loc
        };
  
        const vid2 = this.$route.params.vid;
        fetch(`http://127.0.0.1:5000/api/venueput/${vid2}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
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
      }
    }
  };
  </script>
  
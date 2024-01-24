<template>
    <div>
      <div class="mb-3">
        <label class="form-label">Available tickets</label>
        <label class="form-label">{{ available }}</label>
        <label class="form-label">{{ mid }}</label>
      </div>
      <div>
        <div class="mb-3">
          <label class="form-label">bookings</label>
          <input type="text" class="form-control" v-model="bookings" name="bookings">
        </div>
        <div class="mb-3">
          <label class="form-label">no</label>
          <input type="text" class="form-control" v-model="no" name="no">
        </div>
        <button type="submit" class="btn btn-primary" @click="goTobook">submit</button>
    
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: ['sid'],
    data() {
      return {
        available: '',
        mid: '',
        no: '',
        bookings: '',
        access_token: null,
        uid: null, // Initialize the available tickets count
      };
    },
    methods: {
      extractUidFromToken(token) {
        const parts = token.split('.');
        if (parts.length !== 3) {
          console.error('Invalid token format.');
          return null;
        }
  
        const payloadJson = atob(parts[1]);
        const payload = JSON.parse(payloadJson);
  
        console.log('Token Payload:', payload);
  
        if (!payload.sub.uid) {
          console.error('Uid not found in token payload.');
          return null;
        }
  
        const uid = payload.sub.uid;
  
        return uid;
      },
  
      goTobook() {
        const data = {
          no: this.no,
          bookings: this.bookings,
        };
        this.access_token = localStorage.getItem('access_token');
  
        console.log('Access Token:', this.access_token);
  
        this.uid = this.extractUidFromToken(this.access_token);
  
        console.log('Extracted Uid:', this.uid);
        // Use the correct 'vid' prop from the component's props
        const sid9 = this.$route.params.sid;
        fetch(`http://127.0.0.1:5000/api/bookpost/${sid9}/${this.uid}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        })
          .then((response) => response.json())
          .then((data) => {
            // Update the 'available' data property with the fetched value
            this.mid = data.mid;
            this.available = data.available;
            this.$router.push('/book/' + sid9);
          })
          .catch((error) => {
            // Handle any errors that occur during the fetch (optional)
            console.error('Error fetching available tickets:', error);
          });
      },
    },
    created() {
      // Fetch the number of available tickets from the server when the component is mounted
  
      const sid7 = this.$route.params.sid;
      fetch(`http://127.0.0.1:5000/api/bookget/${sid7}`)
        .then((response) => response.json())
        .then((data) => {
          // Update the 'available' data property with the fetched value
          this.available = data.available;
        })
        .catch((error) => {
          // Handle any errors that occur during the fetch (optional)
          console.error('Error fetching available tickets:', error);
        });
    },
  };
  </script>

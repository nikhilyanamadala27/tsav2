<template>
    <div>
      <div class="mb-3">
        <label class="form-label">username</label>
        <input type="username" class="form-control" v-model="NAME">
        <div id="emailHelp" class="form-text">We'll never share your details with anyone else.</div>
      </div>
      <div class="mb-3">
        <label for="exampleInputPassword1" class="form-label">Password</label>
        <input type="password" class="form-control" id="exampleInputPassword1" v-model="PASSWORD">
      </div>
      <div class="mb-3">
        <label for="exampleInputPassword1" class="form-label">email</label>
        <input type="username" class="form-control" id="exampleInputPassword1" v-model="email">
      </div>
      <button type="submit" class="btn btn-primary" @click="goTousVenue">signin</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        email: '',
        NAME: '',
        PASSWORD: ''
      };
    },
    methods: {
      goTousVenue() {
        const data = {
          email: this.email,
          usname1: this.NAME,
          pass1: this.PASSWORD
        };
  
        fetch('http://127.0.0.1:5000/api/uloginpost', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        }).then(response => {
          if (response.ok) {
            this.$router.push('/userlogin'); // Navigate to the "venue" page
          } else {
            // Handle the response when there's an error (optional)
            console.error('Login failed');
          }
        }).catch(error => {
          // Handle any network errors (optional)
          console.error('Network error:', error);
        });
      }
    }
  };
  </script>
  
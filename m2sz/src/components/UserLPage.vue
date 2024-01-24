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
      <button type="submit" class="btn btn-primary" @click="loginUser">login</button>
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
      loginUser() {
        const data = {
          email: this.email,
          usname1: this.NAME,
          pass1: this.PASSWORD
        };
        const data1 = {
          email: this.email,
          usname1: this.NAME,
          pass1: this.PASSWORD
        };
      
        fetch('http://127.0.0.1:5000/api/loginpostv', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        })
        .then(response => response.json()) // Parse response as JSON
        .then(data => {
          console.log("Response data:", data); // Log the response data to the console
      
          if (data.message === "Login successful") {
            // Store the token in local storage
            localStorage.setItem("access_token", data.access_token);
            console.log("Token stored in localStorage:", localStorage.getItem("access_token"));
             if((data1.usname1 === "NIKHIL" && data1.pass1 === "HII" && data1.email==="yanamadalasainikhil@gmail.com")){
                    this.$router.push('/advenue');
               }else {
                   this.$router.push('/usvenue');} // Navigate to the "venue" page
          } else {
            console.error("Login failed:", data.message);
            this.password_hash = "";
          }
        })
        .catch(error => {
          console.error("Login failed:", error);
          this.password_hash = ""; // Clear the password field on login failure
        });
      }
    }
  };
  </script>
  
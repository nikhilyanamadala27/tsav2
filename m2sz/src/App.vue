<!-- src/App.vue -->
<template>
  <div id="app">
    <div class="container">
      <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <a class="navbar-brand" href="#">Guestbook</a>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/usersignin">Signin</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/userlogin">Login</router-link>
            </li>
          </ul>
        </div>
      </nav>
      <div class="row">
        <div class="col">
          <router-view></router-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
/* Add any global styles here if needed */
</style>

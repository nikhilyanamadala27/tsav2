// src/main.js
import { createApp } from 'vue';
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';

import AdVenue from './components/AdVenue.vue';
import HomePage from './components/HomePage.vue';
import BookPage from './components/BookPage.vue';
import ShowEForm from './components/ShowEForm.vue';
import ShowForm from './components/ShowForm.vue';
import ShowPage from './components/ShowPage.vue';
import UserPage from './components/UserPage.vue';
import UserLPage from './components/UserLPage.vue';
import UShows from './components/UShows.vue';
import USVenue from './components/USVenue.vue';
import VenueForm from './components/VenueForm.vue';
import VenueFormEdit from './components/VenueFormEdit.vue';


// Create the router instance
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomePage },
    { path: '/advenue', component: AdVenue },
    { path: '/book/:sid', component: BookPage },
    { path: '/showeform/:sid', component: ShowEForm },
    { path: '/showform/:vid', component: ShowForm },
    { path: '/showpage/:vid', component: ShowPage },
    { path: '/usersignin', component: UserPage },
    { path: '/userlogin', component: UserLPage },
    { path: '/ushows/:vid', component: UShows },
    { path: '/usvenue', component: USVenue },
    { path: '/venueform', component: VenueForm },
    { path: '/venueformedit/:vid', component: VenueFormEdit },
    
  ],
});

// Create the Vue app instance
const app = createApp(App);

// Use the router instance with the app
app.use(router);

// Mount the app to the #app element
app.mount('#app');

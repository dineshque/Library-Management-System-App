<template>
    <Navbar/>
      <h2 class="h3" style="color: aliceblue;"> Welcome to Stats Dashboard </h2> 
     <libStats  v-if = "userRole=='librarian'"></libStats>
     <userStats  v-if = "userRole=='user'"></userStats>
  </template>
  
  <script>
  import Navbar from './navbaruser.vue'
  import libStats from './libStats.vue'
  import userStats from './userStats.vue'
  export default {
      components:{
        Navbar,
        libStats,
        userStats,
      },
      data(){
        return{
          userRole : localStorage.getItem('role'),
        }
      }
  };
  </script>
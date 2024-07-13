<template>
  <div>
    <Navbar @search="handleSearch" />
    <userDashboard :search_value="search_value"  v-if = "userRole=='user'"/>
    <libDashboard :search_value="search_value" v-if = "userRole=='librarian'"/>
  </div>
</template>

<script>
import Navbar from './navbaruser.vue'
import libDashboard from './libDashboard.vue'
import userDashboard from './userDashboard.vue'

export default {
  
  name:'Dashboard',
  
  data() {
      return{
        userRole : localStorage.getItem('role'),
        search_value:'',
      }
  },
  components:{
      Navbar,
      libDashboard,
      userDashboard,
      
    },
    methods: {
    handleSearch(value) {
      this.search_value = value;
    },
  },
    
};
</script>


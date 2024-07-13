<template>
  <div v-if="alertMessage" class="d-flex banner" style="justify-content: center;">
    <div v-if="alertMessage" class="d-flex flex-row flex-wrap alert container bg-danger bg-gradient text-dark w-50"
      role="alert" style="position: fixed;bottom: 0px; z-index: 99999; justify-content: center; align-items: end;">
      <strong>Notification : </strong> {{ alertMessage['Notification'] }}
      <span type="button" class="position-absolute btn btn-link btn-sm text-dark" @click="clearAlert()"
        style="right: 0; font-size: 1.2rem;"><i class="bi bi-x-circle"></i></span>
    </div>
  </div>

  <nav class="navbar navbar-expand-lg navbar-light p-2 bg-primary">
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item active">
          <router-link class="nav-link" to="/dashboard">
            <h5>{{ current_user }}'s' Dashboard</h5>
          </router-link>
        </li>
      </ul>
      <div class="d-flex ">
        <form class="d-flex" @submit.prevent="handleSearch" action="" method="post">
          <input class="form-control me-2" v-model="search_value" placeholder="Search" aria-label="Search">
          <button class="btn btn-success" type="submit">Search</button>
        </form>
        <router-link class=" nav-link mr-sm-2 mx-3 my-1" v-if="role == 'user'" to="/mybooks">
          <h5>MyBooks</h5>
        </router-link>
        <router-link class=" nav-link mr-sm-2 my-1" v-if="role == 'user'" to="/books">
          <h5>Books</h5>
        </router-link>
        <router-link class=" nav-link mr-sm-2 mx-3 my-1" v-if="role == 'librarian'" @click="clearSearch" to="/bookview">
          <h5>Books</h5>
        </router-link>
        <router-link class=" nav-link mr-sm-2  my-1" v-if="role == 'librarian'" to="/bookrequest">
          <h5>Requests</h5>
        </router-link>
        <router-link class=" nav-link mr-sm-2  my-1" to="stats">
          <h5>Stats</h5>
        </router-link>
        <button v-if="is_login" class="btn btn-secondary my-2 my-sm-0 right-align" @click="handleLogout"> Logout
        </button>
      </div>
    </div>
  </nav>

</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'Navbar',
  data() {
    return {
      role: localStorage.getItem("role"),
      is_login: localStorage.getItem("auth-token"),
      current_user: '',
      search_value: '',
    }
  },
  computed: {
    ...mapGetters(['Username', 'alertMessage']),
  },
  methods: {
    clearSearch() {
      this.search_value = '';
    },
    alertTimer() {
      setTimeout(() => {
        var alertMessage = null;
        this.$store.dispatch("updateAlert", alertMessage)
      }, 3500)
    },
    async handleSearch(value) {
      this.$emit('search', this.search_value);
    },
    async handleLogout() {
      try {
        const response = await fetch('http://localhost:5000/logout', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem("auth-token"),
          },
        });

        if (response.ok) {
          localStorage.removeItem('auth-token');
          localStorage.removeItem('role');
          this.$router.push('/');
        } else {
          var alertMessage = { "Notification": data.message, };

        }
      } catch (error) {
        var alertMessage = { "Notification": error, };
      }
      this.$store.dispatch('updateAlert', alertMessage);
      this.alertTimer();
    },
  },
  async mounted() {

    try {
      const res = await fetch('http://localhost:5000/api/current_profile', {
        headers: {
          'Authentication-Token': localStorage.getItem("auth-token"),
        },
      })
      const data = await res.json();
      if (res.ok) {
        this.current_user = data.User

      } else {
        var alertMessage = { "Notification": data.message, };

      }
    } catch (error) {
      var alertMessage = { "Notification": error, };
    }
    this.$store.dispatch('updateAlert', alertMessage);
    this.alertTimer();
  },
}
</script>

<style scoped>
input {
  background-color: rgb(24, 19, 101);
  color: aliceblue;
}
</style>
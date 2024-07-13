<template>
  <div v-if="alertMessage" class="d-flex banner" style="justify-content: center;">
    <div v-if="alertMessage" class="d-flex flex-row flex-wrap alert container bg-danger bg-gradient text-dark w-50"
      role="alert" style="position: fixed;bottom: 0px; z-index: 99999; justify-content: center; align-items: end;">
      <strong>Notification : </strong> {{ alertMessage['Notification'] }}
      <span type="button" class="position-absolute btn btn-link btn-sm text-dark" @click="clearAlert()"
        style="right: 0; font-size: 1.2rem;"><i class="bi bi-x-circle"></i></span>
    </div>
  </div>

  <div class=" container">

    <div class="row ">
      <div class="col">
        <div class="card">
          <div class="card-header">
            <h4>User Login</h4>
          </div>
          <div class="card-body">
            <form @submit.prevent="loginUser" action="" method="post">
              <div class="form-group">
                <label>Email</label>
                <input type="email" name="email" class="form-control" placeholder="Email" v-model="formData.email"
                  required>
              </div>
              <div class="form-group">
                <label>Password</label>
                <input type="password" class="form-control" name="password" placeholder="Password"
                  v-model="formData.password" required>
              </div>
              <button type="submit" class="btn btn-primary btn-block">Login</button>
              <h3> Don't have account </h3>
              <router-link to="/userregistration">Register here</router-link>
            </form>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      formData: {
        email: '',
        password: '',
        role: 'user'
      },
    };

  },
  computed: {
    ...mapGetters(['alertMessage']),
  },
  methods: {
    alertTimer() {
      setTimeout(() => {
        var alertMessage = null;
        this.$store.dispatch("updateAlert", alertMessage)
      }, 3500)
    },
    async loginUser() {
      console.log("Form Submitted");

      try {
        const res = await fetch('http://localhost:5000/user-login', {
          method: 'post',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.formData),
        });

        const data = await res.json();
        if (res.ok) {
          localStorage.setItem('auth-token', data.token);
          localStorage.setItem('role', data.role);
          this.$router.push({ path: '/dashboard', query: { user: data.username } });
        } else {
          var alertMessage = { "Notification": data.message, };

        }
      } catch (error) {
        var alertMessage = { "Notification": 'Error during login:', error, };

      }
      this.$store.dispatch('updateAlert', alertMessage);
      this.alertTimer();
    },
  },
  mounted() {
    if (localStorage.getItem('auth-token')) {
      this.$router.push('/dashboard');
    }
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
}

.card {
  margin-top: 20%;
  background-color: rgb(213, 195, 171);
  width: 40rem;

}

input {
  background-color: bisque;
}

button {
  background-color: rgba(35, 65, 173, 0.918);
}
</style>
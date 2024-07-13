<template>
  <div class="container">
    <div class="row ">
      <div class="col">
        <div class="card">
          <div class="card-header col-12">
            <h4>Librarian  Login</h4>
          </div>
          <div class="card-body">
            <form @submit.prevent="loginUser" action="" method="post">
              <div class="form-group">
                <label>Email</label> 
                <input type="email" name="email" class="form-control" placeholder="Email" v-model="formData.email" required>
              </div>
              <div class="form-group">
                <label>Password</label>
                <input type="password" class="form-control" name="password" placeholder="Password" v-model="formData.password" required>
              </div>
              <button type="submit" class="btn btn-primary btn-block">Login</button>
            </form>
            <h5 class='text-danger red-star' >{{ error }}</h5>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      formData: {
        email: '',
        password: '',
        role : 'librarian'
      },
      error:null
    };
  },
  methods: {
    async loginUser() {
      try {
        const res = await fetch('http://localhost:5000//user-login', {
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

          // this.$store.dispatch('updateUsername', data.username);

          this.$router.push({path:'/dashboard'});
        } else {
          this.error = data.message
        }
      } catch (error) {
        console.error('Error during login:', error);
      }
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
.container{
  display: flex;
  justify-content: center;
}
.card{
  margin-top: 20%;
  background-color: rgb(213, 195, 171);
  width: 40rem;
}
input{
  background-color:bisque;
}
button{
  background-color: rgba(35, 65, 173, 0.918);
}
</style>
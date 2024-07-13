<template>
  <div style="text-align:center; margin-top:50px">
    <h1>Welcome To LMS </h1> <br><br>

    <h2>
      <router-link to="/adminLogin">Login as a Librarian</router-link> <br><br>
      <router-link to="/userLogin">Login as a User</router-link>
    </h2>

  </div>
</template>
<script>
export default {
  mounted() {
    if (localStorage.getItem('auth-token')) {
      this.$router.push('/dashboard');
    }
  },
}
</script>
<style scoped>
div {
  color: brown;
}
</style>
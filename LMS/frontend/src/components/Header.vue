<template>
    <div>
      <a v-on:click="logout" href="#">Logout</a>
    </div>
</template>

<script>
export default{
    name:  'HeaderTag',
    methods:{
        async logout(){
            console.warn("Logout ??????")
            if (localStorage.getItem('auth-token')){
                localStorage.removeItem('auth-token')
                this.$router.push('/')
    }
        }
    }
}
</script>
<template>
  <div class=" container">
    <div class="row ">
      <div class="col">
        <div class="card " >
          <div class="card-header">
            <h4>Add  Section</h4>
          </div>
          <div class="card-body">
            <form @submit.prevent="sectionAdd" action="" method="post">
              <div class="form-group">
                <label>Title</label> 
                <input type="text" name="title" class="form-control" placeholder="Title" v-model="formData.name" required>
              </div>
              <div class="form-group">
                <label>Description</label>
                <input type="text" class="form-control" name="description" placeholder="Description" v-model="formData.description" required>
              </div>
              <div class="bt">
                <button type="submit" class="btn btn-success mx-3">Add</button>
                <router-link to='/dashboard'><button type="button" class="btn btn-danger mx-3">Cancel</button></router-link>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-if="alertMessage" class="d-flex banner" style="justify-content: center;">
      <div v-if="alertMessage" class="d-flex flex-row flex-wrap alert container bg-danger bg-gradient text-dark w-50" role="alert"
        style="position: fixed;bottom: 0px; z-index: 99999; justify-content: center; align-items: end;">
          <strong>Notification : </strong> {{ alertMessage['Notification'] }}
        <span type="button" class="position-absolute btn btn-link btn-sm text-dark" @click="clearAlert()"
          style="right: 0; font-size: 1.2rem;"><i class="bi bi-x-circle"></i></span>
      </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
  data() {
    return {
      authToken: localStorage.getItem("auth-token"),
      formData: {
        name: '',
        description:"",
      },
    };
   
  },
  computed: {
    ...mapGetters(['alertMessage']),
  },
  methods: {
    clearAlert(){
      var alertMessage = null;
      this.$store.dispatch("updateAlert",alertMessage)
    },
    alertTimer(){
      setTimeout(()=>{
        var alertMessage = null;
      this.$store.dispatch("updateAlert",alertMessage)
      },3500)
    },
    async sectionAdd() {

      try {
        const res = await fetch('http://localhost:5000/api/section', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.authToken,
          },
          body: JSON.stringify(this.formData),
        });

        const data = await res.json();
        if (res.ok) {
          this.$router.push({path:'/dashboard'});
          var alertMessage = {
          "Notification": 'Section Added, Sucessfully',
        };
        
        } else {
          var alertMessage = {
          "Notification": data.response.errors[0],
        };
        }
      } catch (error) {
        var alertMessage = {
          "Notification": data.error,
        };
      }
      this.$store.dispatch('updateAlert', alertMessage);
      this.alertTimer();
    },
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
.bt{
  display: flex;
  justify-content: space-between;
}
</style>
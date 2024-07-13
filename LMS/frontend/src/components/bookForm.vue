<template>
    <div class=" container">
      <div class="row ">
        <div class="col">
          <div class="card" >
            <div class="card-header">
              <h4>Add Book</h4>
            </div>
            <div class="card-body">
              <form @submit.prevent="bookAdd" action="" method="post">
                <div class="form-group">
                  <label>Title</label> 
                  <input type="text" name="title" class="form-control" placeholder="Title" v-model="formData.name" required>
                </div>
                <div class="form-group">
                  <label>Author</label> 
                  <input type="text" name="author" class="form-control" placeholder="Author" v-model="formData.author" required>
                </div>
                <div class="form-group">
                  <label>Content</label>
                  <input type="text" class="form-control" name="content" placeholder="Content" v-model="formData.content" required>
                </div>
                <div class="form-group">
                  <label>Number Of Pages</label> 
                  <input type="number" name="pages" class="form-control" placeholder="No. of Pages" v-model="formData.pages" required>
                </div>
                <div class="form-group">
                  <label>Book Section</label> : {{ sectionName }}
                </div>
                <div class="bt">
                  <button type="submit" class="btn btn-success mx-3">Add</button>
                  <h5 class='text-danger red-star' >{{ error }}</h5>
                  <router-link to='/dashboard'><button type="button" class="btn btn-danger mx-3">Cancel</button></router-link>
                </div>
              </form>
              
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: ['sectionID','sectionName'],
    data() {
      return {
        formData: {
          name: '',
          author: '',
          content:"",
          pages:'',
        },
        error : null
      };
     
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
      async bookAdd() {
  
        try {
          const res = await fetch(`http://localhost:5000/api/book/${this.sectionID}`, {
            method: 'post',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.formData),
          });
  
          const data = await res.json();
          if (res.ok) {
            var alertMessage = {"Notification": data.message };
            this.$router.push({path:'/dashboard'});
          } else {
            // this.error = data.message
            var alertMessage = {"Notification": data.message };
          }
        } catch (error) {
          // console.error('Error during login:', error);
          var alertMessage = {"Notification": error };
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
  /* button{ */
    /* background-color: rgba(35, 65, 173, 0.918); */
  /* } */
  .bt{
    display: flex;
    justify-content: space-between;
  }
  </style>
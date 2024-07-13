<template>

  <div class="container mt-5">
    <div v-if="alertMessage" class="d-flex banner" style="justify-content: center;">
      <div v-if="alertMessage" class="d-flex flex-row flex-wrap alert container bg-danger bg-gradient text-dark w-50"
        role="alert" style="position: fixed;bottom: 0px; z-index: 99999; justify-content: center; align-items: end;">
        <strong>Notification : </strong> {{ alertMessage['Notification'] }}
        <span type="button" class="position-absolute btn btn-link btn-sm text-dark" @click="clearAlert()"
          style="right: 0; font-size: 1.2rem;"><i class="bi bi-x-circle"></i></span>
      </div>
    </div>

    <div class="row justify-content-center">

      <div v-if="section.length !== 0" v-for="v in filteredSections" :key="v.section_id" class="col-md-4 mb-5">

        <div class="card">

          <div class="card-header col-12">
            <h4> {{ v.name }} </h4>

          </div>

          <div class="card-body">
            <h5> Date : {{ new Date(v.date).toLocaleDateString('en-US', {
              year: 'numeric', month: '2-digit', day:
              '2-digit' }) }}</h5>

            <p>{{ v.description }}</p>

            <div class="bt">
              <router-link :to="{ name: 'bookView', params: { sectionID: v.section_id } }"><button
                  class="btn btn-info">View Books</button></router-link>
              <button @click="showAddBookModal(v.section_id, v.name)" class="btn btn-success">Add Book</button>
            </div>

            <div class="bt mt-3">
              <router-link :to="{ name: 'editSection', params: { sectionID: v.section_id } }">
                <button class="btn btn-warning">Edit</button>
              </router-link>
              <button @click="deleteSection(v.section_id)" class="btn btn-danger">Delete</button>
            </div>

          </div>
        </div>
      </div>
      <div class="h3" style="color: aliceblue;" v-else>No Sections Created</div>
    </div>
  </div>

  <div class="d-flex justify-content-center">
    <router-link to="/addsection" class="btn btn-warning">Add Section</router-link>
  </div>

  <!-- Add Book Modal -->
  <div class="modal" :class="{ 'is-active': showModal }">

    <div class="modal-background" @click="showModal = false"></div>

    <div class="modal-content">

      <div class="card">

        <div class="card-header">
          <h4>Add Book</h4>
        </div>

        <div class="card-body">

          <form @submit.prevent="bookAdd" action="" method="post">
            <div class="d-flex justify-content-center">
              <h4> <label>Book Section</label> : {{ selectedSectionName }} </h4>
            </div>

            <div class="form-group">
              <label>Title</label>
              <input type="text" name="title" class="form-control" placeholder="Title" v-model="BookData.name" required>
            </div>
            <div class="form-group">
              <label>Author</label>
              <input type="text" name="author" class="form-control" placeholder="Author" v-model="BookData.author"
                required>
            </div>

            <div class="form-group">
              <label>Content</label>
              <input type="text" class="form-control" name="content" placeholder="Content" v-model="BookData.content"
                required>
            </div>

            <div class="form-group">
              <label>Number Of Pages</label>
              <input type="number" name="pages" class="form-control" placeholder="No. of Pages" v-model="BookData.pages"
                required>
            </div>

            <div class="bt">
              <button type="submit" class="btn btn-success mx-3">Add</button>
              <button type="button" @click="showModal = false" class="btn btn-danger  mx-3">Cancel</button>
            </div>

          </form>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: "libDashboard",
  props: ['search_value'],
  data() {
    return {
      authToken: localStorage.getItem("auth-token"),
      section: [],
      showModal: false,
      selectedSectionID: null,
      selectedSectionName: null,
      BookData: {
        name: '',
        author: '',
        content: "",
        pages: "",
      },
    }
  },
  computed: {
    ...mapGetters(['alertMessage']),
    filteredSections() {
      if (!this.search_value) {
        return this.section ;
      } else {
        return this.section.filter(sec =>
          sec.name.toLowerCase().includes(this.search_value.toLowerCase())
        );
      }
    },
  },
  methods: {
    clearAlert() {
      var alertMessage = null;
      this.$store.dispatch("updateAlert", alertMessage)
    },
    alertTimer() {
      setTimeout(() => {
        var alertMessage = null;
        this.$store.dispatch("updateAlert", alertMessage)
      }, 3500)
    },
    async deleteSection(selectedSectionID) {
      try {
        const res = await fetch(`http://localhost:5000/api/section/${selectedSectionID}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.authToken,
          }
        });
        const data = await res.json();
        if (res.ok) {
          this.section = this.section.filter(sec => sec.section_id !== selectedSectionID);
          var alertMessage = {
            "Notification": data.message,
          };

        } else {
          var alertMessage = {
            "Notification": data.message,
          };
        }
      } catch (error) {
        var alertMessage = {
          "Notification": 'An error occurred while deleting the section.',
        };
      }
      this.$store.dispatch('updateAlert', alertMessage);
      this.alertTimer();
    },
    showAddBookModal(sectionID, sectionName) {
      this.selectedSectionID = sectionID;
      this.selectedSectionName = sectionName;
      this.showModal = true;
    },
    async bookAdd() {

      try {
        const res = await fetch(`http://localhost:5000/api/book_section/${this.selectedSectionID}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.authToken,
          },
          body: JSON.stringify(this.BookData),
        });

        const data = await res.json();
        if (res.ok) {
          this.showModal = false;
          this.BookData.name = '';
          this.BookData.author = '';
          this.BookData.content = '';
          this.BookData.pages = '';
          var alertMessage = {
            "Notification": data.message,
          };

        } else {
          var alertMessage = {
            "Notification": data.message,
          };

        }
      } catch (error) {
        var alertMessage = {
          "Notification": error,
        };
      }
      this.$store.dispatch('updateAlert', alertMessage);
      this.alertTimer();
    },
  },
  async mounted() {
    const res = await fetch('http://localhost:5000/api/section', {
      headers: {
        'Authentication-Token': this.authToken,
      },
    })
    const data = await res.json()
    if (res.ok) {
      this.section = data.reverse()
    } else {
      alert(data.message)
    }
  },
};
</script>

<style scoped>
input {
  background-color: bisque;
}

.container {
  color: black;

}

.bt {
  display: flex;
  justify-content: space-between;
}
</style>

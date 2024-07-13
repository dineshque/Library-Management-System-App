<template>
  <Navbar @search="handleSearch" />
  <div class="h4 d-flex justify-content-center my-3">
    <h4 style="color: aliceblue;" class="mx-2 my-auto"> Filter By : </h4>
    <select v-model="filterBy" name="filterby" style="font-size: 1.2rem;" class="btn btn-warning">
      <option value="name">Book Name</option>
      <option value="author">Author Name</option>
    </select>
  </div>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div v-if="book.length !== 0" v-for="v in filteredBooks" :key="v.book_id" class="col-md-4 mb-5">
        <div class="card">
          <div v-if="v.rated > 0" class="card-header d-flex justify-content-between col-12">
            <h4> {{ v.name }} </h4>
            <h4 style="color: brown;" class=""> {{ v.rated }} <i class="bi bi-star-fill"></i></h4>
          </div>
          <div v-else class="card-header d-flex justify-content-between col-12">
            <h4> {{ v.name }} </h4>
          </div>
          <div class="card-body">
            <h5> Author : {{ v.author }}</h5>

            <div class="bt mt-3">
              <button @click="showAddBookModal(v.book_id, v.name)" class="btn btn-warning">Edit </button>
              <button @click="deleteBook(v.book_id)" class="btn btn-danger">Delete</button>
            </div>
          </div>
        </div>
      </div>
      <div class="h3" style="color: aliceblue;" v-else>No books added</div>
    </div>

    <div v-if="alertMessage" class="d-flex banner" style="justify-content: center;">
      <div v-if="alertMessage" class="d-flex flex-row flex-wrap alert container bg-danger bg-gradient text-dark w-50"
        role="alert" style="position: fixed;bottom: 0px; z-index: 99999; justify-content: center; align-items: end;">
        <strong>Notification : </strong> {{ alertMessage['Notification'] }}
        <span type="button" class="position-absolute btn btn-link btn-sm text-dark" @click="clearAlert()"
          style="right: 0; font-size: 1.2rem;"><i class="bi bi-x-circle"></i></span>
      </div>
    </div>
  </div>
  <!-- Edit Book Modal -->
  <div class="modal" :class="{ 'is-active': showModal }">

    <div class="modal-background" @click="showModal = false"></div>

    <div class="modal-content">

      <div class="card">

        <div class="card-header">
          <h4>Edit Book</h4>
        </div>

        <div class="card-body">

          <form @submit.prevent="bookEdit" action="" method="post">

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
              <label>Number of Pages</label>
              <input type="number" class="form-control" name="pages" placeholder="No. of Pages" v-model="BookData.pages"
                required>
            </div>

            <div class="bt">
              <button type="submit" class="btn btn-success mx-3">Done</button>
              <button type="button" @click="showModal = false" class="btn btn-danger  mx-3">Cancel</button>
            </div>

          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from './navbaruser.vue'
import { mapGetters } from 'vuex';
export default {
  name: "bookView",
  props: ['sectionID', 'search_value'],
  components: {
    Navbar,
  },
  data() {
    return {
      authToken: localStorage.getItem('auth-token'),
      book: [],
      showModal: false,
      selectedBookID: null,
      selectedBookName: null,
      search_value: '',
      BookData: {
        name: '',
        author: '',
        content: "",
        pages: "",
      },
      filterBy: 'name',
    }
  },
  computed: {
    ...mapGetters(['alertMessage']),
    filteredBooks() {

      if (!this.search_value || this.search_value == '') {
        return this.book;
      } else {

        return this.book.filter(sec =>
          sec[this.filterBy].toLowerCase().includes(this.search_value.toLowerCase())
        );


      }
    },
  },
  methods: {
    handleFilter(criteria) {
      this.filterBy = criteria;
    },
    handleSearch(value) {
      this.search_value = value;
    },
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
    async deleteBook(selectedBookID) {
      try {
        const res = await fetch(`http://localhost:5000/api/book/${selectedBookID}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.authToken,
          }
        });
        const data = await res.json();
        if (res.ok) {
          this.book = this.book.filter(sec => sec.book_id !== selectedBookID);
          alert(data.message);
        } else {
          var alertMessage = {
            "Notification": data['response']['errors'][0],
          };
        }
      } catch (error) {

        var alertMessage = {
          "Notification": 'An error occurred while deleting the book.',
        };
      }
      this.$store.dispatch('updateAlert', alertMessage);
      this.alertTimer();
    },
    showAddBookModal(bookID, bookName) {

      this.selectedbookID = bookID;
      this.selectedbookName = bookName;
      this.showModal = true;
    },
    async bookEdit() {

      try {
        const res = await fetch(`http://localhost:5000/api/book/${this.selectedbookID}`, {
          method: 'PUT',
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
          await this.loadBookData();

        } else {
          this.error = data.message
          var alertMessage = {
            "Notification": data['response']['errors'][0],
          };
        }
      } catch (error) {
        var alertMessage = {
          "Notification": 'Error During Updating Book',
        };
      }
      this.$store.dispatch('updateAlert', alertMessage);
      this.alertTimer();
    },
    async loadBookData() {

      var res = await fetch(`http://localhost:5000/api/book`, {
        headers: {
          'Authentication-Token': this.authToken,
        },
      })

      const data = await res.json()
      if (res.ok) {
        this.book = data.reverse()
      } else {
        alert(data.message)
      }
    }
  },

  async mounted() {
    if (localStorage.getItem('role') == 'librarian') {
      await this.loadBookData();
      if (this.$route.query.search_value){
        this.search_value = this.$route.query.search_value;
      }
      
    }
    else {
      this.$router.push({ path: '/dashboard' });

      var alertMessage = {
        "Notification": 'You are not allowed to access this Page',
      };

      this.$store.dispatch('updateAlert', alertMessage);
      this.alertTimer();
    }

  },
};
</script>

<style scoped>
input {
  background-color: bisque;
}

.bt {
  display: flex;
  justify-content: space-between;
}

container {
  color: azure;
}
</style>

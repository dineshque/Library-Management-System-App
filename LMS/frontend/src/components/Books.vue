<template>
  <Navbar @search="handleSearch" />
  <div class="container mt-5">
    <div class="h4 d-flex justify-content-center my-3">
      <h4 style="color: aliceblue;" class="mx-2 my-auto"> Filter By : </h4>
      <select v-model="filterBy" name="filterby" style="font-size: 1.2rem;" class="btn btn-warning">
        <option value="name">Book Name</option>
        <option value="author">Author Name</option>
        <option value="section_name">Section Name</option>
      </select>
    </div>

    <div class="row justify-content-center">
      <div v-if="book.length !== 0" v-for="v in filteredBooks" :key="v.book_id" class="col-12 mb-4">
        <div class="card">
          <div class="card-header d-flex col-12">
            <h4 v-if="v.rated > 0" style="color:darkred;"> {{ v.name }} | {{ v.author }} | {{ v.section_name }} <span
                class="mx-3"> {{ v.rated }} <i class="bi bi-star-fill"></i></span></h4>
            <h4 v-else style="color:darkred;"> {{ v.name }} | {{ v.author }} | {{ v.section_name }} </h4>
            <div class="ms-auto">
              <form class="d-flex-inline" @submit.prevent="handleRequest(v.book_id)" action="" method="post">
                <label class="h6 mx-2" for="day">No. of Days : </label>
                <input id="day" type="number" v-model="day[v.book_id]" min="0" max="15" required></input>
                <button type="submit" class="btn btn-success mx-3">Request</button>
              </form>
            </div>
          </div>
        </div>
      </div>
      <div class="h3" style="color: aliceblue;" v-else>No books Available</div>
    </div>

    <div class="h3" style="color: aliceblue;">Requested Books</div>

    <div class="row justify-content-center">
      <div v-if="requested_books.length !== 0" v-for="v in filtered_requested_Books" :key="v.book_id"
        class="col-12 mb-4">
        <div class="card">
          <div class="card-header d-flex col-12">
            <h4 style="color:darkred;"> {{ v.book_name }} | {{ v.author }} | {{ v.section_name }} </h4>
            <div class="ms-auto">
              <button type="button" class="btn btn-secondary mx-3" disabled>Requested</button>
            </div>
          </div>
        </div>
      </div>
      <div class="h3" style="color: aliceblue;" v-else>No books Available</div>
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
</template>

<script>
import Navbar from './navbaruser.vue'
import { mapGetters } from 'vuex';
export default {
  name: "bookView",
  props: ['search_value'],
  components: {
    Navbar,
  },
  data() {
    return {
      authToken: localStorage.getItem('auth-token'),
      book: [],
      requested_books: [],
      search_value: '',
      filterBy: 'name',
      day: {},
    }
  },
  computed: {
    ...mapGetters(['alertMessage']),
    filteredBooks() {

      if (!this.search_value) {
        return this.book;
      } else {
        return this.book.filter(sec =>
          sec[this.filterBy].toLowerCase().includes(this.search_value.toLowerCase())
        );

      }
    },
    filtered_requested_Books() {


      if (!this.search_value) {
        return this.requested_books;
      } else {
        if (this.filterBy == 'name'){
          return this.requested_books.filter(sec =>
          sec['book_name'].toLowerCase().includes(this.search_value.toLowerCase())
        );
        }else{
          return this.requested_books.filter(sec =>
          sec[this.filterBy].toLowerCase().includes(this.search_value.toLowerCase())
        );
        }
        
      }
    },
  },
  methods: {
    handleFilter(criteria) {
      this.filterBy = criteria;
    },
    async handleRequest(book_id) {
      try {
        const res = await fetch(`http://localhost:5000/api/user_book/${book_id}`, {
          method: 'post',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.authToken,
          },
          body: JSON.stringify({ "book_status": 1, "days": this.day[book_id] }),
        });

        const data = await res.json();
        if (res.ok) {
          await this.currentBookData();
          await this.requstedBookData();
          var alertMessage = { "Notification": data.message };

        } else {
          var alertMessage = { "Notification": data.message };
        }
      } catch (error) {
        var alertMessage = { "Notification": error };
      }
      this.$store.dispatch('updateAlert', alertMessage);
      this.alertTimer();
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
    async currentBookData() {

      var res = await fetch(`http://localhost:5000/api/book`, {
        headers: {
          'Authentication-Token': this.authToken,
        },
      })

      const data = await res.json()
      if (res.ok) {
        this.book = data.reverse()
      } else {
        var alertMessage = {
          "Notification": data.message,
        };
      }
      this.$store.dispatch('updateAlert', alertMessage);
      this.alertTimer();
    },
    async requstedBookData() {

      var res = await fetch(`http://localhost:5000/api/user_book/Requested`, {
        headers: {
          'Authentication-Token': this.authToken,
        },
      })

      const data = await res.json()
      if (res.ok) {
        this.requested_books = data
      } else {
        var alertMessage = {
          "Notification": data.message,
        };
      }
      this.$store.dispatch('updateAlert', alertMessage);
      this.alertTimer();
    }
  },

  async mounted() {
    await this.currentBookData();
    await this.requstedBookData();
  },
};
</script>

<style scoped>
input {
  background-color: bisque;
}

</style>

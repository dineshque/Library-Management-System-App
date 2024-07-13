<template>
  <Navbar @search="handleSearch" />
  <div class="container mt-5">
    <div class="h4 d-flex justify-content-center my-3">
      <h4 style="color: aliceblue;" class="mx-2 my-auto"> Filter By : </h4>
      <select v-model="filterBy" name="filterby" style="font-size: 1.2rem;" class="btn btn-warning">
        <option value="book_name">Book Name</option>
        <option value="author">Author Name</option>
        <option value="section_name">Section Name</option>
      </select>
    </div>
    <div class="h3" style="color: aliceblue;">Current Books</div>

    <div class="row justify-content-center">
      <div v-if="book.length !== 0" v-for="v in filteredBooks" :key="v.book_id" class="col-12 mb-4">
        <div class="card">
          <div class="card-header d-flex col-12">
            <h4 style="color:darkred;"> {{ v.book_name }} | {{ v.author }} | {{ v.section_name }} </h4>
            <div class="ms-auto">
              <form class="d-flex-inline" @submit.prevent="returnBook(v.user_id, v.book_id)" action="" method="post">
                <label class="h6 mx-2" for="rate">Rate : </label>
                <input id="rate" type="number" v-model="rate[v.book_id]" min="0" max="10" required></input>
                <button type="submit" class="btn btn-success mx-3">Return</button>
              </form>
            </div>
          </div>
        </div>
      </div>
      <div class="h3" style="color: aliceblue;" v-else>No books Available</div>
    </div>

    <div class="h3" style="color: aliceblue;">Completed Books</div>

    <div class="row justify-content-center">
      <div v-if="completed_book.length !== 0" v-for="v in filtered_completed_Books" :key="v.book_id"
        class="col-12 mb-4">
        <div class="card">
          <div class="card-header d-flex col-12">
            <h4 style="color:darkred;"> {{ v.book_name }} | {{ v.author }} | {{ v.section_name }} </h4>
            <div class="ms-auto">
              <span class="h5 mx-3">Rated : {{ v.rate }} <i class="bi bi-star-fill"></i></span>
              <button type="button"
                @click="showAddBookModal(v.book_name, v.section_name, v.rate, v.return_date, v.issued_date)"
                class="btn btn-success ">View</button>
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

  <!-- View Book Modal -->
  <div class="modal" :class="{ 'is-active': showModal }">

    <div class="modal-background" @click="showModal = false"></div>

    <div class="modal-content">

      <div class="card">

        <div class="card-header">
          <h4 class="m-auto">Details</h4>
        </div>

        <div class="card-body">
          <h4>Book Name : {{ selected_data['book_name'] }} </h4>
          <h4 class="my-3">Book Section : {{ selected_data['section_name'] }} </h4>
          <h4 class="my-3">Rated : {{ selected_data['rate'] }} <i class="bi bi-star-fill"></i> </h4>
          <h4 class="my-3">Issued Date : {{ selected_data['issued_date'] }} </h4>
          <h4 class="my-3">Return Date : {{ selected_data['return_date'] }} </h4>
          <div class="d-flex justify-content-end">
            <button type="button" @click="showModal = false" class="btn btn-danger  mx-3">Cancel</button>
          </div>
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
  props: [ 'search_value'],
  components: {
    Navbar,
  },
  data() {
    return {
      authToken: localStorage.getItem('auth-token'),
      book: [],
      completed_book: [],
      showModal: false,
      search_value: '',
      rate: {},
      selected_data: {
        book_name: '',
        rate: '',
        section_name: '',
        return_date: '',
        issued_date: '',
      },
      filterBy: 'book_name',
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
    filtered_completed_Books() {
      if (!this.search_value) {
        return this.completed_book;
      } else {

        return this.completed_book.filter(sec =>
          sec[this.filterBy].toLowerCase().includes(this.search_value.toLowerCase())
        );


      }
    },
  },
  methods: {
    handleFilter(criteria) {
      this.filterBy = criteria;
    },
    async returnBook(user_id, book_id) {
      try {
        const res = await fetch(`http://localhost:5000/api/user_book/${user_id}/${book_id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.authToken,
          },
          body: JSON.stringify({ "book_status": 4, "rate": this.rate[book_id] }),
        });

        const data = await res.json();
        if (res.ok) {
          var alertMessage = { "Notification": data.message };
          window.location.reload();
        } else {
          var alertMessage = { "Notification": data.message };
        }
      } catch (error) {
        var alertMessage = { "Notification": error };
      }
      this.$store.dispatch('updateAlert', alertMessage);
      this.alertTimer();
    },
    showAddBookModal(book_name, section_name, rate, return_date, issued_date) {
      this.selected_data['book_name'] = book_name;
      this.selected_data['section_name'] = section_name;
      this.selected_data['rate'] = rate;
      this.selected_data['return_date'] = return_date;
      this.selected_data['issued_date'] = issued_date;
      this.showModal = true;
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
    async loadBookData() {

      var res = await fetch(`http://localhost:5000/api/user_book/Granted`, {
        headers: {
          'Authentication-Token': this.authToken,
        },
      })

      var res1 = await fetch(`http://localhost:5000/api/user_book/Completed`, {
        headers: {
          'Authentication-Token': this.authToken,
        },
      })

      const data = await res.json()
      const data1 = await res1.json()
      if (res.ok) {
        this.book = data
        this.completed_book = data1
      } else {
        alert(data.message)
        var alertMessage = {
          "Notification": data.message,
        };
      }
      this.$store.dispatch('updateAlert', alertMessage);
      this.alertTimer();
    }
  },

  async mounted() {
    await this.loadBookData();
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

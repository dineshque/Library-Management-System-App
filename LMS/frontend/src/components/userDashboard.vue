<template>
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
            <h4 style="color:darkred;"> {{ v.book_name }} | {{ v.author }} | {{ v.section_name }} </h4>
            <div class="ms-auto">
              <button type="button" @click="readBook(v.book_id)" class="btn btn-success mx-3">Read</button>
            </div>
          </div>
        </div>
      </div>
      <div class="h3" style="color: aliceblue;" v-else>No books Available For Reading</div>
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
  <!-- Book Detail Modal -->
  <div class="modal" :class="{ 'is-active': showModal }">

    <div class="modal-background" @click="showModal = false"></div>

    <div class="modal-content">

      <div class="card">
        <div class="card-header col-12">
          <h4> {{ v.name }} </h4>
        </div>
        <div class="card-body">
          <h5> Author : {{ v.author }}</h5>
          <p> ------------------------------------------------------- </p>
          <p>{{ v.content }}</p>
          <p> ------------------------------------------------------- </p>

          <div class="bt mt-3 d-flex justify-content-between">
            <span>P. No. : {{ v.pages }}</span>
            <button type="button" @click="showModal = false" class="btn btn-danger  mx-3">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
  name: "userDashboard",
  props: ['search_value'],

  data() {
    return {
      authToken: localStorage.getItem('auth-token'),
      book: [],
      v: '',
      error: null,
      filterBy: 'name',
      // dropdownOpen: true,
      showModal: false,
    }
  },
  computed: {
    ...mapGetters(['alertMessage']),
    filteredBooks() {
      console.log('Search Value:', this.search_value);
      console.log('Books:', this.book);

      if (!this.search_value) {
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

    async readBook(book_id) {
      this.showModal = true;
      var res = await fetch(`http://localhost:5000/api/book/${book_id}`, {
        headers: {
          'Authentication-Token': this.authToken,
        },
      })

      const data = await res.json()
      if (res.ok) {
        // this.book = data
        this.v = data

      } else {
        // alert(data.message)
        var alertMessage = {
          "Notification": data.message,
        };
      }
      this.$store.dispatch('updateAlert', alertMessage);
      this.alertTimer();
    },

    async loadBookData() {

      var res = await fetch(`http://localhost:5000/api/user_book/Granted`, {
        headers: {
          'Authentication-Token': this.authToken,
        },
      })

      const data = await res.json()
      if (res.ok) {
        this.book = data.filter(sec => sec.book_status == 2);
      } else {
        alert(data.message)
      }
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

<template>
  <Navbar @search="handleSearch" />
  <div class="container mt-5">

    <div class="h4 d-flex justify-content-center my-3">
      <h4 style="color: aliceblue;" class="mx-2 my-auto"> Filter By : </h4>
      <select v-model="filterBy" name="filterby" style="font-size: 1.2rem;" class="btn btn-warning">
        <option value="book_name">Book Name</option>
        <option value="user_name">User Name</option>
      </select>
    </div>

    <div class="row justify-content-center">
      <div class="h3" style="color: aliceblue;">Books Requested</div>

      <div v-if="book.length !== 0" v-for="v in filteredBooks" :key="v.book_id" class="col-12 mb-4">
        <div class="card">
          <div class="card-header d-flex col-12">
            <h4 style="color:darkred;"> {{ v.book_name }} | {{ v.user_name }} </h4>
            <div class="ms-auto">
              <button type="button"
                @click="showAddBookModal(v.book_id, v.book_status, v.book_name, v.user_name, v.days, v.section_name)"
                class="btn btn-info">See Detail</button>
              <button type="button" @click="rejectRequest(v.user_id, v.book_id)"
                class="btn btn-danger mx-3">Reject</button>
              <button type="button" @click="grantRequest(v.user_id, v.book_id)"
                class="btn btn-success mx-3">Grant</button>
            </div>
          </div>
        </div>
      </div>

      <div class="h3" style="color: aliceblue;" v-else>No Books Here</div>

      <div class="h3" style="color: aliceblue;">Granted Books</div>

      <div v-if="granted_book.length !== 0" v-for="v in filteredgrantedBooks" :key="v.book_id" class="col-12 mb-4">
        <div class="card">
          <div class="card-header d-flex col-12">
            <h4 style="color:darkred;"> {{ v.book_name }} | {{ v.user_name }} </h4>
            <div class="ms-auto">
              <button type="button"
                @click="showAddBookModal(v.book_id, v.book_status, v.book_name, v.user_name, v.days, v.section_name)"
                class="btn btn-info">See Detail</button>
              <button type="button" @click="revokeBook(v.user_id, v.book_id)"
                class="btn btn-danger mx-3">Revoke</button>
            </div>
          </div>
        </div>
      </div>
      <div class="h3" style="color: aliceblue;" v-else>No Books Here</div>

      <!-- completed Books -->
      <div class="h3" style="color: aliceblue;">Completed Books</div>
      <div v-if="completed_book.length !== 0" v-for="v in filteredcompletedBooks" :key="v.book_id" class="col-12 mb-4">
        <div class="card">
          <div class="card-header d-flex col-12">
            <h4 style="color:darkred;"> {{ v.book_name }} | {{ v.user_name }} </h4>
            <div class="ms-auto">
              <button type="button"
                @click="showAddBookModal(v.book_id, v.book_status, v.book_name, v.user_name, v.days, v.section_name, v.rate, v.return_date, v.issued_date)"
                class="btn btn-info">See Detail</button>
            </div>
          </div>
        </div>
      </div>
      <div class="h3" style="color: aliceblue;" v-else>No Books Here</div>

      <!-- Revoked Books -->

      <div class="h3" style="color: aliceblue;">Revoked Books</div>
      <div v-if="revoked_book.length !== 0" v-for="v in filteredrevokedBooks" :key="v.book_id" class="col-12 mb-4">
        <div class="card">
          <div class="card-header d-flex col-12">
            <h4 style="color:darkred;"> {{ v.book_name }} | {{ v.user_name }} </h4>
            <div class="ms-auto">
              <button type="button"
                @click="showAddBookModal(v.book_id, v.book_status, v.book_name, v.user_name, v.days, v.section_name, v.rate, v.return_date, v.issued_date)"
                class="btn btn-info">See Detail</button>
              <button v-if="showCancelButton(v.return_date, v.issued_date, v.days)" type="button"
                @click="cancelrevoke(v.user_id, v.book_id)" class="btn btn-danger mx-3">Cancel Revoke</button>
              <button v-else type="button" class="btn btn-secondary mx-3" disabled>Revoked</button>
            </div>
          </div>
        </div>
      </div>
      <div class="h3" style="color: aliceblue;" v-else>No Books Here</div>
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

  <!-- Book User Detail Modal -->
  <div v-if="selected_data['book_status'] === 1 || selected_data['book_status'] === 2" class="modal"
    :class="{ 'is-active': showModal }">

    <div class="modal-background" @click="showModal = false"></div>

    <div class="modal-content">

      <div class="card">

        <div class="card-header">
          <h4 class="m-auto">Details</h4>
        </div>

        <div class="card-body">
          <h4>Username : {{ selected_data['user_name'] }} </h4>
          <h4 class="my-3">Days Requested : {{ selected_data['day'] }} </h4>
          <h4 class="my-3">Book Title : {{ selected_data['book_name'] }} </h4>
          <h4 class="my-4">Book Section : {{ selected_data['section_name'] }} </h4>
          <div class="d-flex justify-content-between">
            <button type="button" class="btn btn-warning mx-3" @click="viewBook(selected_data['book_name'])">View
              Book</button>
            <button type="button" @click="showModal = false" class="btn btn-danger  mx-3">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Completed Book Detail Modal -->
  <div v-if="selected_data['book_status'] == 4" class="modal" :class="{ 'is-active': showModal }">

    <div class="modal-background" @click="showModal = false"></div>

    <div class="modal-content">

      <div class="card">

        <div class="card-header">
          <h4 class="m-auto">Details</h4>
        </div>

        <div class="card-body">
          <h4>Username : {{ selected_data['user_name'] }} </h4>
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

  <!-- Revoked Book Detail Modal -->
  <div v-if="selected_data['book_status'] == 3" class="modal" :class="{ 'is-active': showModal }">

    <div class="modal-background" @click="showModal = false"></div>

    <div class="modal-content">

      <div class="card">

        <div class="card-header">
          <h4 class="m-auto">Details</h4>
        </div>

        <div class="card-body">
          <h4>Username : {{ selected_data['user_name'] }} </h4>
          <h4>Book Name : {{ selected_data['book_name'] }} </h4>
          <h4 class="my-3">Book Section : {{ selected_data['section_name'] }} </h4>
          <h4 class="my-3">Rated : {{ selected_data['rate'] }} <i class="bi bi-star-fill"></i> </h4>
          <h4 class="my-3">Issued Date : {{ selected_data['issued_date'] }} </h4>
          <h4 class="my-3">Revoked Date : {{ selected_data['return_date'] }} </h4>
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
      granted_book: [],
      completed_book: [],
      revoked_book: [],
      showModal: false,
      search_value: '',
      filterBy: 'book_name',
      selected_data: {
        book_id: '',
        book_name: '',
        user_name: '',
        day: '',
        section_name: '',
        book_status: '',
        rate: '',
        return_date: '',
        issued_date: '',
      }
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
    filteredgrantedBooks() {

      if (!this.search_value) {
        return this.granted_book;
      } else {

        return this.granted_book.filter(sec =>
          sec[this.filterBy].toLowerCase().includes(this.search_value.toLowerCase())
        );


      }
    },
    filteredcompletedBooks() {

      if (!this.search_value) {
        return this.completed_book;
      } else {

        return this.completed_book.filter(sec =>
          sec[this.filterBy].toLowerCase().includes(this.search_value.toLowerCase())
        );


      }
    },
    filteredrevokedBooks() {

      if (!this.search_value) {
        return this.revoked_book;
      } else {

        return this.revoked_book.filter(sec =>
          sec[this.filterBy].toLowerCase().includes(this.search_value.toLowerCase())
        );


      }
    },

  },
  methods: {
    handleFilter(criteria) {
      this.filterBy = criteria;
      this.dropdownOpen = true;
    },
    handleSearch(value) {
      this.search_value = value;
    },

    async grantRequest(user_id, book_id) {
      try {
        const res = await fetch(`http://localhost:5000/api/user_book/${user_id}/${book_id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.authToken,
          },
          body: JSON.stringify({ "book_status": 2 }),
        });

        const data = await res.json();
        if (res.ok) {
          var alertMessage = { "Notification": data.message };
          await this.loadBookData();
        } else {
          var alertMessage = { "Notification": data.message };
        }
      } catch (error) {
        var alertMessage = { "Notification": error };
      }
      this.$store.dispatch('updateAlert', alertMessage);
      this.alertTimer();
    },
    async rejectRequest(user_id, book_id) {
      try {
        const res = await fetch(`http://localhost:5000/api/user_book/${user_id}/${book_id}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.authToken,
          },
        });

        const data = await res.json();
        if (res.ok) {
          this.book = this.book.filter(sec => sec.book_id !== book_id);
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
          "Notification": 'An error occurred while reject Request.',
        };
      }
      this.$store.dispatch('updateAlert', alertMessage);
      this.alertTimer();
    },
    async revokeBook(user_id, book_id) {
      try {
        const res = await fetch(`http://localhost:5000/api/user_book/${user_id}/${book_id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.authToken,
          },
          body: JSON.stringify({ "book_status": 3 }),
        });

        const data = await res.json();
        if (res.ok) {
          await this.loadBookData();
          this.book = this.book
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
          "Notification": 'An error occurred while deleting the book.',
        };
      }
      this.$store.dispatch('updateAlert', alertMessage);
      this.alertTimer();
    },
    async cancelrevoke(user_id, book_id) {
      try {
        const res = await fetch(`http://localhost:5000/api/user_book/${user_id}/${book_id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.authToken,
          },
          body: JSON.stringify({ "book_status": 2 }),
        });

        const data = await res.json();
        if (res.ok) {
          await this.loadBookData();
          this.book = this.book
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
          "Notification": 'An error occurred while Cancel Revoke.',
        };
      }
      this.$store.dispatch('updateAlert', alertMessage);
      this.alertTimer();
    },
    async viewBook(book_name) {

      this.$router.push({ name: 'booksView', query: { search_value: book_name } });
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
     showAddBookModal(book_id = null, book_status = null, book_name = null, user_name = null, day = null, section_name = null, rate = null, return_date = null, issued_date = null) {
      this.selected_data['book_id'] = book_id;
      this.selected_data['book_name'] = book_name;
      this.selected_data['user_name'] = user_name;
      this.selected_data['day'] = day;
      this.selected_data['rate'] = rate;
      this.selected_data['section_name'] = section_name;
      this.selected_data['book_status'] = book_status;
      this.selected_data['return_date'] = return_date;
      this.selected_data['issued_date'] = issued_date;
      this.showModal = true;
    },
    showCancelButton(return_date, issued_date, days) {

      if (return_date && issued_date) {
        const returnDate = new Date(return_date);
        const issuedDate = new Date(issued_date);
        const daysToAdd = days;
        const tempIssuedDate = new Date(issuedDate);
        tempIssuedDate.setDate(tempIssuedDate.getDate() + daysToAdd);
        return returnDate < tempIssuedDate;
      }

      return false;
    },
    async loadBookData() {

      var res = await fetch(`http://localhost:5000/api/user_book`, {
        headers: {
          'Authentication-Token': this.authToken,
        },
      })

      const data = await res.json()
      if (res.ok) {
        this.book = data.filter(sec => sec.book_status == 1);
        this.granted_book = data.filter(sec => sec.book_status == 2);
        this.completed_book = data.filter(sec => sec.book_status == 4);
        this.revoked_book = data.filter(sec => sec.book_status == 3);

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
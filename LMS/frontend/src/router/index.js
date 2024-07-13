import { createRouter, createWebHistory } from 'vue-router'
import user from '../components/userLogin.vue'
import Home from '../components/Home.vue'
import Profile from '../components/profile.vue'
import Login from '../components/adminLogin.vue'
import Useruserregistration from '../components/Useruserregistration.vue'
import Dashboard from '../components/dashboard.vue'
import MyBooks from '../components/MyBooks.vue'
import Stats from '../components/Stats.vue'
import Books from '../components/Books.vue'
import addSection from '../components/sectionForm.vue'
import addBook from '../components/bookForm.vue'
import bookView from '../components/bookView.vue'
import booksView from '../components/booksView.vue'
import editSection from '../components/editSectionForm.vue'
import bookRequest from '../components/bookRequested.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: Profile
    },
    {
      path: '/adminlogin',
      name: 'login',
      component: Login
    },
    {
      path: '/userlogin',
      name: 'userlogin',
      component: user
    },
    {
      path: '/userregistration',
      name: 'Userregistration',
      component: Useruserregistration
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard
    },
    {
      path: '/mybooks',
      name: 'MyBooks',
      component: MyBooks
    },
    {
      path: '/books',
      name: 'Books',
      component: Books,
    },
    {
      path: '/stats',
      name: 'Stats',
      component: Stats
    },
    {
      path: '/addsection',
      name: 'addSection',
      component : addSection
    },
    {
      path: '/editsection/:sectionID',
      name: 'editSection',
      component : editSection,
      props: true
    },

    {
      path: '/addbook/:sectionID',
      name: 'addBook',
      component: addBook,
      props: true
    },
    {
      path: '/bookview/:sectionID',
      name: 'bookView',
      component : bookView,
      props: true
    },
    {
      path: '/bookview',
      name: 'booksView',
      component : booksView,
      props: true
    },
    {
      path: '/bookrequest',
      name: 'bookRequest',
      component : bookRequest,
      props: true
    },
  ]
})

router.beforeEach((to, from, next) => {
  if ((to.name !== 'home' && to.name !== 'userlogin' && to.name !== 'login' && to.name !== 'Userregistration' ) && !localStorage.getItem('auth-token')) {
    next({ name: 'home' }) 
  } else {
    next() 
  }
})



export default router

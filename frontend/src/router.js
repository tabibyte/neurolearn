import { createRouter, createWebHistory } from 'vue-router'

// Import views
import Home from './views/home.vue'
import Dyslexia from './views/dyslexia.vue'
import ADHD from './views/adhd.vue'
import Autism from './views/autism.vue'
import Dyscalculia from './views/dyscalculia.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/dyslexia',
    name: 'Dyslexia',
    component: Dyslexia
  },
  {
    path: '/adhd',
    name: 'ADHD',
    component: ADHD
  },
  {
    path: '/autism',
    name: 'Autism',
    component: Autism
  },
  {
    path: '/dyscalculia',
    name: 'Dyscalculia',
    component: Dyscalculia
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
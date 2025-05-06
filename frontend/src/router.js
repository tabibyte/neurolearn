import { createRouter, createWebHistory } from 'vue-router'

// Import views
import Home from './views/home.vue'
import ResourceList from './views/resourcelist.vue'
import AIAssistant from './views/aiassistant.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/resources',
    name: 'Resources',
    component: ResourceList
  },
  {
    path: '/ai-assistant',
    name: 'AIAssistant',
    component: AIAssistant
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
import { createRouter, createWebHistory } from 'vue-router'
import DiffPathDisplay from '@/views/DiffPathDisplay.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/editor' },
    { path: '/diff', name: 'DiffPath', component: DiffPathDisplay },
  ]
})

export default router

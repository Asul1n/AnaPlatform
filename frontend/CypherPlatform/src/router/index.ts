import { createRouter, createWebHistory } from 'vue-router'
import CypherEditor from '../views/CypherEditor.vue'
import DiffPathDisplay from '@/views/DiffPathDisplay.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/editor' },
    { path: '/editor', component: CypherEditor },
    { path: '/diff', name: 'DiffPath', component: DiffPathDisplay },
  ]
})

export default router

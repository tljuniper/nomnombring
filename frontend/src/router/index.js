import { createRouter, createWebHistory } from 'vue-router'
import RecipeList from '../components/RecipeList.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'recipes',
      component: RecipeList
    },
  ]
})

export default router

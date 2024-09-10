<template>
  <div>
    <div>
      <h1>NomNomBring</h1>
      <form @submit.prevent="submitRecipes">
        <button type="submit" class="recipeButton">
          Add to shopping list
        </button>
        <div class="wrap-search">
          <label for="search" class="input-text">
            <input type=search id="search" v-model="search" placeholder="Search..." />
          </label>
        </div>
      </form>
    </div>
    <div class="recipe-list">
      <recipe-list-item v-for="(recipe) in recipes" :key="recipe.id" :title="recipe.title" :id="recipe.id"
        :active="recipe.active" v-show="isVisible(recipe)" @recipe-selected="selectRecipe">
      </recipe-list-item>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import RecipeListItem from "./RecipeListItem.vue";

class Recipe {
  constructor(title, id, active) {
    this.title = title;
    this.id = id;
    this.active = active;
  }
}

export default {
  data() {
    return {
      recipes: [],
      search: '',
    };
  },
  components: {
    'recipe-list-item': RecipeListItem,
  },
  methods: {
    selectRecipe(payload) {
      let recipe = this.recipes.find(recipe => (payload.id == recipe.id));
      recipe.active = payload.active;
      this.recipes.sort((a, b) => {
        return b.active - a.active;
      });
    },
    getRecipes() {
      console.log("getRecipes()");
      axios
        .get("/recipes")
        .then((res) => {
          let newRecipes = [];
          res.data.recipes.forEach((recipe) => {
            newRecipes.push(new Recipe(recipe.title, recipe.id, false));
          });
          this.recipes = newRecipes;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    submitRecipes() {
      let filteredRecipes = this.recipes.filter(recipe => recipe['active']);

      let payload = [];
      let recipe_list = [];
      filteredRecipes.forEach(recipe => {
        payload.push(recipe.id)
        recipe_list.push(recipe.title);
      });

      this.clearButtonStates();
      this.clearSearch();

      console.log("Active recipes: " + recipe_list.join(", "))
      alert("Adding: " + recipe_list.join(", "));

      axios.post("/recipes", payload).catch((error) => {
        console.log(error);
        alert("Something went wrong :(")
      });
    },
    clearSearch() {
      this.search = '';
    },
    clearButtonStates() {
      this.recipes.forEach(recipe => {
        recipe['active'] = false;
      });
    },
    isVisible(recipe) {
      return recipe.title.toLowerCase().includes(this.search.toLowerCase());
    }
  },
  created() {
    this.getRecipes();
  },
};
</script>

<style>
h1 {
  text-align: center;
}

.recipeButton {
  border-style: none;
  color: white;
  background-color: #455C64;
  width: 100%;
  margin-top: 5px;
  margin-bottom: 5px;
  padding: 15px;
  font-size: 20px;
}

input[type="search"] {
  width: 100%;
  font-size: 20px;
}

.input-text {
  width: auto;
  display: block;
  margin: 0 auto;
}

.wrap-search {
  width: 100%;
  margin-top: 5px;
  margin-bottom: 5px;
}

.recipe-list {
  margin-top: 10px;
  margin-bottom: 10px;
}
</style>

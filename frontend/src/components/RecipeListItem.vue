<template>
  <button type="button" v-on:click="selectRecipe()" class="recipe" v-bind:class="{ active: active }">
    {{ title }}
  </button>
</template>

<script>
export default {
  emits: ['recipe-selected'],
  props: ['title', 'id', 'active'],
  methods: {
    selectRecipe: function () {
      this.$emit('recipe-selected', { id: this.id, active: !this.active });
    }
  },
};
</script>

<style scoped>
.recipe {
  text-align: left;
  border-style: none;
  color: white;
  background-color: #73BAAE;
  width: 100%;
  margin-top: 5px;
  margin-bottom: 5px;
  padding: 6px;
  padding-left: 15px;
  padding-right: 15px;
  font-size: 18px;
}

.active {
  background-color: #F16A68;
}
</style>

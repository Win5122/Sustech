<template>
  <div class="App">
    <Usage/>
    <Login/>
  </div>
</template>

<script setup>
import Usage from './components/Usage.vue'
import Login from './components/Login.vue'
</script>

<style>
.App {
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
}
</style>

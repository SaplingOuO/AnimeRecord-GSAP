<!-- 參考網頁 https://www.palmer-dinnerware.com/ -->
<script setup>
import animeData from './assets/MyProject/gamerAcg-List.json'
// import HelloWorld from './components/HelloWorld.vue'
// import ScrollBox from './components/ScrollBox.vue'
import ObserverBox from './components/ObserverBox.vue'
</script>

<template>
  <ObserverBox :animes="animeData" />
  <!-- <ScrollBox /> -->
  <!-- <HelloWorld :animes="animeData"/> -->
</template>

<style>
</style>

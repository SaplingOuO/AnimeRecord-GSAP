<!-- 參考網頁 https://www.palmer-dinnerware.com/ -->
<script setup>
import animeData from './assets/MyProject/gamerAcg-List.json'
// import HelloWorld from './components/HelloWorld.vue'
import TestS from './components/TestS.vue'
// import ObserverBox from './components/ObserverBox.vue'
</script>

<template>
  <!-- <HelloWorld :animes="animeData"/> -->
  <TestS :animes="animeData"/>
  <!-- <ObserverBox :animes="animeData" /> -->
</template>

<style>
</style>

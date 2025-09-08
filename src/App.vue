<!-- 參考網頁 https://www.palmer-dinnerware.com/ -->
<script setup>
import animeData from './assets/MyProject/gamerAcg-List.json'
import HelloWorld from './components/HelloWorld.vue'
import BackgroundVideo from './components/BackgroundVideo.vue'
// import ObserverBox from './components/ObserverBox.vue'
</script>

<!-- <template> -->
  <!-- <HelloWorld :animes="animeData"/> -->
  <!-- <ObserverBox :animes="animeData" /> -->
<!-- </template> -->

<template>
  <!-- 菜單 -->
  <div></div>

  <!-- 主畫面 -->
  <div>
    <!-- 背景影片or圖片 -->
    <!-- <BackgroundVideo :animes="animeData"/> -->

    <!-- 畫面中央 -->
    <div></div>

    <!-- 底部橫向卷軸 -->
    <HelloWorld/>

    <!-- 側邊縱向卷軸 -->
     <div></div>
  </div>
</template>

<style>
</style>

<!-- 參考網頁 https://www.palmer-dinnerware.com/ -->
<script setup>
import { ref } from 'vue'
import animeData from './assets/MyProject/gamerAcg-List.json'
import BackgroundVideo from './components/BackgroundVideo.vue'
import CardList from './components/CardList.vue'
import YearList from './components/YearList.vue'

const selectedYear = ref(null);

function handleSelectedYear(year) {
  console.log("中央年份:", year);
  selectedYear.value = year;
}
</script>

<template>
  <!-- 菜單 -->
  <div></div>

  <!-- 主畫面 -->
  <div>
    <!-- 背景影片or圖片 -->
    <BackgroundVideo :animes="animeData"/>

    <!-- 畫面中央 -->
    <div></div>

    <!-- 底部橫向卷軸 -->
    <CardList :year="selectedYear" />

    <!-- 側邊縱向卷軸 -->
    <YearList @update:selected="handleSelectedYear" />
    
  </div>
</template>

<style>
  body{
    background-color: rgba( 0, 0, 0, 0.2) !important;
  }
</style>

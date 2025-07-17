<script setup>
import Animes from "../assets/MyProject/gamerAcg-List.json";
import { ref } from 'vue'

defineProps({
  msg: String,
})

const count = ref(0)
const animes = ref(Animes)

</script>

<template>
  <div v-for="anime in animes" :key="anime.num">
    <h3>{{ anime.cn }}（{{ anime.en }}）</h3>
    <p>發售日：{{ anime.releaseDate }} | 季節：{{ anime.season }}</p>
    <img :src="`../animeImages/${anime.image}`" alt="cover" />
  </div>
</template>

<style scoped>

</style>

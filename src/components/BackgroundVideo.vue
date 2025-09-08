<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { checkYoutubeVideo, createYoutubePlayer } from '../services/youtube'
import { searchAnime } from '../services/jikan'

const props = defineProps({
  animes: {
    type: Array,
    required: false,
    default: () => []
  }
})

const hasYoutube = ref(false)
const backgroundImage = ref(null) // fallback 圖片
let player = null

async function getPlayableYoutubeId(randomAnime) {
  const list = await searchAnime(randomAnime.en)
  const getId = list[0]?.trailer?.youtube_id ?? null
  if(!getId){
    console.warn(`⚠️ ${randomAnime.en} 沒有找到 Youtube ID，使用圖片當背景`)
    return null
  } 
  const check = await checkYoutubeVideo(getId)
  if(check.playable){
    return getId
  }else{
    console.warn(`⚠️ 找到的影片不可播放 (${getId})，原因：${check.reason}`)
    return null
  }
}

async function getAnimeImage(randomAnime) {
  const list = await searchAnime(randomAnime.en)
  const animeImage = list[0]?.images?.jpg?.image_url
  backgroundImage.value = animeImage || `../animeImages/${randomAnime.image}`
  return backgroundImage.value
}


onMounted(async () => {
  const randomAnime = props.animes[Math.floor(Math.random() * props.animes.length)]
  const youtubeId = await getPlayableYoutubeId(randomAnime)

  if (youtubeId) {
    hasYoutube.value = true
    player = await createYoutubePlayer('video', youtubeId, 1, 1, 0, 0, 1)
  } else {
    hasYoutube.value = false
    getAnimeImage(randomAnime)
  }
})

onBeforeUnmount(() => {
  if (player && typeof player.destroy === 'function') {
    player.destroy()
  }
})
</script>


<template>
    <div v-if="hasYoutube">
      <div id="video"></div>
    </div>
    <img id="backgroundImage" v-else :src="backgroundImage"/>
</template>

<style>
#video {
  position: fixed;
  top: 0;
  left: -50vw;
  width: 200vw;
  height: 100vh;
  z-index: -1; /* 放到背景 */
  pointer-events: none; /* 防止影片擋住操作 */
  opacity: 0.2;
}
#backgroundImage{
  position: fixed;
  top: 50%;
  left: 50%;
  height: 100vh;
  transform: translate(-50%, -50%);
  z-index: -1; /* 放到背景 */
  pointer-events: none; /* 防止影片擋住操作 */
  opacity: 0.2;
}
</style>
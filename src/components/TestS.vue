<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { createYoutubePlayer } from '../services/youtube'
import { searchAnime } from '../services/jikan'

const props = defineProps({
  animes: {
    type: Array,
    required: false,
    default: () => []
  }
})

const animes = ref([])
let player = null

onMounted(async () => {
  const list = await searchAnime(props.animes[Math.floor(Math.random()*props.animes.length)].en) // 等待 API 回傳結果
  player = await createYoutubePlayer('video', list[0].trailer.youtube_id, 1, 1, 0, 0, 1)
})

onBeforeUnmount(() => {
  if (player && typeof player.destroy === 'function') {
    player.destroy()
  }
})
</script>


<template>
  <!-- 菜單 -->
  <div></div>

  <!-- 主畫面 -->
  <div>
    <!-- 背景影片 -->
    <div>
      <div id="video"></div>
    </div>
    <!-- 畫面中央 -->
    <div></div>
    <!-- 底部橫向卷軸 -->
    <div></div>
  </div>
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
</style>
<template>
  <div class="gallery-container" ref="container">
    <div
      v-for="item in animes"
      :key="item.num"
      class="gallery-item"
      :style="{ backgroundImage: `url(${getImageUrl(item.image)})` }"
      @click="showDetail(item)"
    ></div>

    <!-- 詳細資訊視窗 -->
    <div v-if="selectedItem" class="modal" @click="selectedItem = null">
      <div class="modal-content" @click.stop>
        <h2>{{ selectedItem.cn }}</h2>
        <p>日文：{{ selectedItem.jp }}</p>
        <p>英文：{{ selectedItem.en }}</p>
        <p>發售日：{{ selectedItem.releaseDate }}</p>
        <p>季度：{{ selectedItem.season }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import gsap from 'gsap'
import { Observer } from 'gsap/Observer'
gsap.registerPlugin(Observer)
defineProps({
  animes: Object,
})

const container = ref(null)
let observer

const selectedItem = ref(null)
const showDetail = item => {
  selectedItem.value = item
}

const getImageUrl = filename => `../animeImages/${filename}` // 換成你實際圖片路徑

onMounted(() => {
  const el = container.value
  let pos = { x: 0, y: 0 }

  observer = Observer.create({
    target: window,
    type: 'pointer,touch',
    onDrag: self => {
      pos.x += self.deltaX
      pos.y += self.deltaY

      gsap.set(el, {
        x: `+=${self.deltaX}`,
        y: `+=${self.deltaY}`,
      })

      // 👉 到邊緣時載入更多資料（此處只做示意）
      if (Math.abs(pos.x) > 500 || Math.abs(pos.y) > 500) {
        loadMoreItems()
        pos = { x: 0, y: 0 }
      }
    },
    lockAxis: false,
    inertia: false,
  })
})

onUnmounted(() => {
  if (observer) observer.kill()
})

function loadMoreItems() {
  // 你可以從 API 或本地 JSON 載入更多圖片
  items.value.push(
    ...[
      {
        cn: '追加資料1',
        jp: '追加1',
        en: 'Extra Data 1',
        image: '0000123000.jpg',
        num: '0000123000',
        releaseDate: '2025年08月01日',
        season: '夏季',
      },
      // 更多項目...
    ]
  )
}
</script>

<style scoped>
.gallery-container {
  display: flex;
  flex-wrap: wrap;
  width: 300vw; /* 初始可滾動寬度 */
  height: 300vh;
  overflow: hidden;
  position: relative;
  cursor: grab;
  touch-action: none;
}

.gallery-item {
  width: 180px;
  height: 240px;
  margin: 8px;
  background-size: cover;
  background-position: center;
  border-radius: 12px;
  transition: transform 0.3s ease;
}
.gallery-item:hover {
  transform: scale(1.1);
}

/* 詳細視窗樣式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 12px;
}
</style>
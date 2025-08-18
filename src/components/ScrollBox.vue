<!-- ScrollBox.vue
<template>
  <div class="container">
    <div class="spacer">（這裡是滾動前的空白區域）</div>
    <div class="box" ref="box">Hello GSAP + ScrollTrigger</div>
    <div class="spacer">（這裡是滾動後的空白區域）</div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import gsap from 'gsap'
import ScrollTrigger from 'gsap/ScrollTrigger'

// 註冊 ScrollTrigger plugin
gsap.registerPlugin(ScrollTrigger)

// 取得元素 DOM 參考
const box = ref(null)

onMounted(() => {
  // 建立動畫並搭配 ScrollTrigger
  gsap.from(box.value, {
    x: -200,           // 從左邊位移 200px
    opacity: 0,        // 從透明開始
    duration: 1.5,     // 動畫時間 1.5 秒
    scrollTrigger: {
      trigger: box.value,     // 觸發點：這個元素
      start: 'top 80%',       // 當 box 的頂部到達視窗 80% 高的位置時觸發
      end: 'bottom 60%',      // 可加上 end 點控制動畫範圍（非必要）
      toggleActions: 'play none none none', // 動畫啟動方式
      // 順序分別為: onEnter, onLeave, onEnterBack, onLeaveBack
    }
  })
})
</script>

<style scoped>
.container {
  width: 100%;
  padding: 0 20px;
}

.spacer {
  height: 100vh;
  background-color: #f0f0f0;
}

.box {
  width: 300px;
  height: 100px;
  background-color: #4CAF50;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  margin: 0 auto;
  border-radius: 10px;
}
</style> -->

<template>
  <div class="box" ref="box">拖我 / 滾我 / 按方向鍵</div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import gsap from 'gsap'
import { Observer } from 'gsap/Observer'

gsap.registerPlugin(Observer)

const box = ref(null)

onMounted(() => {
  Observer.create({
    target: window,
    type: 'wheel,pointer,touch,keys',
    onWheel: (self) => {
      let scaleChange = self.deltaY > 0 ? -0.1 : 0.1
      gsap.to(box.value, { scale: '+=' + scaleChange, duration: 0.2 })
    },
    onDrag: (self) => {
      gsap.to(box.value, {
        x: `+=${self.deltaX}`,
        y: `+=${self.deltaY}`,
        duration: 0.1,
        overwrite: true
      })
    },
    onKeyDown: (self) => {
      if (self.key === 'ArrowRight') gsap.to(box.value, { rotation: '+=15' })
      if (self.key === 'ArrowLeft') gsap.to(box.value, { rotation: '-=15' })
    },
    preventDefault: true,
  })
})
</script>

<style scoped>
.box {
  width: 200px;
  height: 200px;
  background: orange;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 12px;
  font-weight: bold;
}
</style>
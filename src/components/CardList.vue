<script setup>
/* ---------------- Props ---------------- */
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from "vue";
import { gsap } from "gsap";
import { Draggable } from "gsap/Draggable";
import { InertiaPlugin } from "gsap/InertiaPlugin";
import { getAnimeByYear, animesList } from "../services/gamerAcg";

// 啟用 GSAP 插件
gsap.registerPlugin(Draggable, InertiaPlugin);

// 父層傳入的參數
const props = defineProps({
  year: String,          // 當前年份 (用來篩選動畫)
});

/* ---------------- State / Data ---------------- */
const listRef = ref(null);   // UL 容器參考
let draggable = null;        // GSAP Draggable 實例
let snapPoints = [];         // 每張卡片能吸附到中心的位置

/* ---------------- Computed ---------------- */
//從gamerAcg.js抓取最新年份資料 or 所有年份資料
const animes = computed(() =>
  props.year ? getAnimeByYear(props.year) : animesList
);

/* ---------------- Methods ---------------- */
// 取得所有 <li.item>
function getItems() {
  const ul = listRef.value;
  return ul ? Array.from(ul.querySelectorAll(".item")) : [];
}
// 計算每張卡片吸附到螢幕中心的 snap 點
function getSnapPoints() {
  const items = getItems();
  console.log("items:", items);

  const screenCenterX = window.innerWidth / 2;
  console.log("screenCenterX:", screenCenterX);

  const points = [];
  let offset = 0;

  items.forEach((item, index) => {
    const cardWidth = item.offsetWidth || 0;
    console.log(`item ${index} width:`, cardWidth);
    const cardCenter = offset + cardWidth / 2;
    points.push(screenCenterX - cardCenter);
    offset += cardWidth;
  });

  console.log("snapPoints:", points);
  return points;
}

// 更新縮放效果：越接近中心 → scale 越大
function updateScale() {
  const items = getItems();
  const ulX = draggable?.x ?? 0;
  const screenCenterX = document.documentElement.clientWidth / 2;
  let offset = 0;

  items.forEach(item => {
    const cardWidth = item.offsetWidth || 0;
    const cardCenter = ulX + offset + cardWidth / 2;
    const distance = Math.abs(screenCenterX - cardCenter);

    const maxDistance = cardWidth * 1.5; // 超過這距離就不縮放
    const scale = gsap.utils.clamp(1, 1.2, gsap.utils.mapRange(0, maxDistance, 1.2, 1)(distance));

    gsap.set(item, { scale });
    offset += cardWidth;
  });
}

// 初始化 / 重新建立 Draggable
function initDraggable() {
  const ul = listRef.value;
  if (!ul) return;

  // 先清掉舊的 Draggable
  if (draggable) {
    draggable.kill();
    draggable = null;
  }

  snapPoints = getSnapPoints();
  if (!snapPoints.length) return; // 如果沒有卡片，直接跳出

  [draggable] = Draggable.create(ul, {
    type: "x",
    edgeResistance: 0.8,
    inertia: true,
    bounds: { 
      minX: snapPoints[snapPoints.length - 1],
      maxX: snapPoints[0]
    },
    snap: { x: snapPoints },
    onDrag: updateScale,
    onThrowUpdate: updateScale,
    onRelease: updateScale,
    onThrowComplete: () => updateScale.call(draggable)
  });

  // 初始化時，強制更新縮放效果
  updateScale.call(draggable);
}

// 對齊第一張卡片到中心
function centerFirstItem(animated = true) {
  if (!draggable || !snapPoints.length) return;
  const targetX = snapPoints[0];

  if (animated) {
    gsap.to(draggable.target, {
      x: targetX,
      duration: 0.6,
      ease: "power2.out",
      onUpdate: () => updateScale.call(draggable),
      onComplete: () => {
        draggable.x = targetX;
        draggable.update();
        updateScale.call(draggable);
      }
    });
  } else {
    gsap.set(draggable.target, { x: targetX });
    draggable.x = targetX;
    draggable.update();
    updateScale.call(draggable);
  }
}

// 窗口大小改變時，重新計算 snapPoints 與邊界
function handleResize() {
  if (!draggable) return;
  snapPoints = getSnapPoints();

  if (snapPoints.length) {
    draggable.applyBounds({
      minX: snapPoints[snapPoints.length - 1],
      maxX: snapPoints[0]
    });
    draggable.vars && (draggable.vars.snap = { x: snapPoints });
    updateScale.call(draggable);
  }
}

/* ---------------- Lifecycle ---------------- */
onMounted(async () => {
  await nextTick();

  // 等圖片加載完
  const images = listRef.value.querySelectorAll("img");
  await Promise.all(Array.from(images).map(img => {
    if (img.complete) return Promise.resolve();
    return new Promise(resolve => img.onload = resolve);
  }));

  initDraggable();
  centerFirstItem(false);
});

// 每次 animes (動畫列表) 改變時，重新初始化並吸附第一張
watch(animes, async () => {
  await nextTick(); 
  initDraggable();
  centerFirstItem(true);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize);
  if (draggable) {
    try { draggable.kill(); } catch (e) {}
    draggable = null;
  }
});
</script>

<template>
  <div class="center-line-vertical"></div> <!-- 螢幕中線 -->
  <div class="container m-0 p-0 position-absolute">
    <ul ref="listRef" class="item-list m-0 position-absolute d-flex list-unstyled">
      <li class="item" v-for="anime in animes" :key="anime.num">
        <img
          class="item-img img-fluid"
          :src="`./animeImages/${anime.image}`"
          :alt="anime.cn"
          loading="lazy"
        />
      </li>
    </ul>
  </div>
</template>

<style scoped>
.container {
  bottom: 30vh;
  z-index: 10; 
}
.item {
  flex: 0 0 auto; 
  padding: 0; 
}
.item-list {
  gap: 2vw; /* 用 gap 代替 padding */
}
.item-img {
  height: 25vh;
  max-width: 177px;
  width: auto;
  object-fit: contain;
}
.center-line-vertical {
  position: absolute;
  height: 100vh;
  left: 50%;
  width: 2px;
  background: rgba(255, 0, 0, 0.6);
  transform: translateX(-50%);
  z-index: 9999;
}
</style>

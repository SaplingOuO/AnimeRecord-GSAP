<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from "vue";
import { gsap } from "gsap";
import { Draggable } from "gsap/Draggable";
import { InertiaPlugin } from "gsap/InertiaPlugin";
import { getAnimeByYear, animesList } from "../services/gamerAcg";

gsap.registerPlugin(Draggable, InertiaPlugin);

const listRef = ref(null);
let draggable = null;
let snapPoints = [];

const props = defineProps({ year: String });

const animes = computed(() => (props.year ? getAnimeByYear(props.year) : animesList));

/* ---------- 公用函式：動態從 DOM 取得項目並計算 snapPoints ---------- */
function getItems() {
  const ul = listRef.value;
  return ul ? Array.from(ul.querySelectorAll(".item")) : [];
}

function getSnapPoints() {
  const items = getItems();
  const screenCenterX = window.innerWidth / 2;
  const points = [];
  let offset = 0;
  items.forEach(item => {
    const cardWidth = item.offsetWidth || 0;
    const cardCenter = offset + cardWidth / 2;
    points.push(screenCenterX - cardCenter);
    offset += cardWidth;
  });
  return points;
}

/* ---------- 縮放計算，改為每次動態取得 items ---------- */
function updateScale() {
  const items = getItems();
  const ulX = (this && this.x) ?? (draggable && draggable.x) ?? 0;
  const screenCenterX = window.innerWidth / 2;
  let offset = 0;
  items.forEach(item => {
    const cardWidth = item.offsetWidth || 0;
    const cardCenter = ulX + offset + cardWidth / 2;
    const distance = Math.abs(screenCenterX - cardCenter);
    const scale = gsap.utils.mapRange(0, Math.max(1, cardWidth * 1.2), 1.2, 1)(distance);
    gsap.set(item, { scale });
    offset += cardWidth;
  });
}

/* ---------- (重新)初始化 Draggable ---------- */
function initDraggable() {
  const ul = listRef.value;
  if (!ul) return;

  // kill 之前的 instance（避免殘留）
  if (draggable) {
    try { draggable.kill(); } catch (e) {}
    draggable = null;
  }

  snapPoints = getSnapPoints();

  // 若沒有 snapPoints（可能無 items）提前返回
  if (!snapPoints.length) return;

  [draggable] = Draggable.create(ul, {
    type: "x",
    edgeResistance: 0.8,
    inertia: true,
    bounds: { minX: snapPoints[snapPoints.length - 1], maxX: snapPoints[0] },
    snap: { x: snapPoints },
    onDrag: updateScale,
    onThrowUpdate: updateScale,
    onRelease: updateScale,
    onThrowComplete: () => {
      updateScale.call(draggable);
    }
  });

  // 立即將 scale 計算一次（使用 draggable 的 x）
  updateScale.call(draggable);
}

/* ---------- 對齊第一張（動畫+更新縮放） ---------- */
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
        // 🔑 動畫完成時強制同步 Draggable 狀態
        draggable.x = targetX;
        draggable.update();
        updateScale.call(draggable);
      }
    });
  } else {
    gsap.set(draggable.target, { x: targetX });
    draggable.x = targetX;   // 🔑 同步數值
    draggable.update();
    updateScale.call(draggable);
  }
}

/* ---------- 當元件掛載：初始化（若資料尚未渲染，使用 nextTick） ---------- */
onMounted(async () => {
  await nextTick();
  initDraggable();
  centerFirstItem(false); // 預設先瞬間對齊（或改 true 動畫）
  window.addEventListener("resize", handleResize);
});

/* ---------- 當 animes 改變（例如換年份）時：等 DOM 完成後重新 init 並回到第一張 ---------- */
watch(animes, async () => {
  await nextTick(); // 等 v-for DOM 更新完成
  // 等 init 完後對齊第一張（動畫）
  centerFirstItem(true);
  // 重新初始化 Draggable（kill + create）
  initDraggable();
});

/* ---------- 窗口尺寸變化處理：重新計算 bounds & snap ---------- */
function handleResize() {
  if (!draggable) return;
  snapPoints = getSnapPoints();
  if (snapPoints.length) {
    draggable.applyBounds({ minX: snapPoints[snapPoints.length - 1], maxX: snapPoints[0] });
    draggable.vars && (draggable.vars.snap = { x: snapPoints });
    updateScale.call(draggable);
  }
}

onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize);
  if (draggable) {
    try { draggable.kill(); } catch (e) {}
    draggable = null;
  }
});
</script>

<template>
  <div class="container m-0 p-0 position-absolute">
    <ul ref="listRef" class="item-list m-0 position-absolute d-flex list-unstyled">
      <li class="item" v-for="anime in animes" :key="anime.num">
        <img class="item-img img-fluid" :src="`/animeImages/${anime.image}`" :alt="anime.cn" loading="lazy" />
      </li>
    </ul>
  </div>
</template>

<style scoped>
.container { bottom: 30vh; z-index: 10; }
.item { flex: 0 0 auto; padding: 2vw; }
.item-img {
  height: 25vh;
  max-width: 177px;
  width: auto;
  object-fit: contain;
}
</style>
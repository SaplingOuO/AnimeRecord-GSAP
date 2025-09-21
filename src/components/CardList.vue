<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from "vue";
import { gsap } from "gsap";
import { Draggable } from "gsap/Draggable";
import { InertiaPlugin } from "gsap/InertiaPlugin";
import { getAnimeByYear, animesList } from "../services/gamerAcg";

gsap.registerPlugin(Draggable, InertiaPlugin);

const listRef = ref(null);
let draggable = null;
let snapPoints = [];
let screenCenterX = window.innerWidth / 2;

const props = defineProps({
  year: String
});

const animes = computed(() => {
  if (!props.year) {
    return animesList;
  } else {
    return getAnimeByYear(props.year);
  }
});

onMounted(() => {
  const ul = listRef.value;

  function getSnapPoints() {
    const items = ul.querySelectorAll(".item");
    let points = [];
    let offset = 0;
    items.forEach(item => {
      const cardWidth = item.offsetWidth || 150; // 預設寬度避免圖片還沒載入
      const cardCenter = offset + cardWidth / 2;
      points.push(screenCenterX - cardCenter);
      offset += cardWidth;
    });
    return points;
  }

  function initDraggable() {
    snapPoints = getSnapPoints();
    [draggable] = Draggable.create(ul, {
      type: "x",
      edgeResistance: 0.8,
      inertia: true,
      bounds: { minX: snapPoints[snapPoints.length - 1], maxX: snapPoints[0] },
      snap: { x: snapPoints },
      onDrag: updateScale,
      onThrowUpdate: updateScale
    });
    updateScale.call({ target: ul, x: draggable.x });
  }

  function updateScale() {
    const items = ul.querySelectorAll(".item");
    const ulX = this.x ?? draggable?.x ?? 0;
    let offset = 0;
    items.forEach(item => {
      const cardWidth = item.offsetWidth || 150;
      const cardCenter = ulX + offset + cardWidth / 2;
      const distance = Math.abs(screenCenterX - cardCenter);
      const scale = gsap.utils.mapRange(0, cardWidth * 1.2, 1.2, 1)(distance);
      gsap.set(item, { scale });
      offset += cardWidth;
    });
  }

  function handleResize() {
    screenCenterX = window.innerWidth / 2;
    snapPoints = getSnapPoints();
    if (draggable) {
      draggable.applyBounds({ minX: snapPoints[snapPoints.length - 1], maxX: snapPoints[0] });
      draggable.vars.snap = { x: snapPoints };
      updateScale.call(draggable);
    }
  }

  function centerFirstItem() {
    if (draggable && snapPoints.length > 0) {
      gsap.to(draggable.target, {
        x: snapPoints[0],
        duration: 0.6,
        onUpdate: () => updateScale.call(draggable),
        onComplete: () => updateScale.call(draggable)
      });
      draggable.update();
    }
  }

  // 🟢 初始化就能拖曳
  initDraggable();
  window.addEventListener("resize", handleResize);
  centerFirstItem();

  // 🟢 圖片載入後會更新 snapPoints 與縮放
  ul.querySelectorAll("img").forEach(img => {
    img.addEventListener("load", () => {
      snapPoints = getSnapPoints();
      handleResize();
    });
  });

  // 🟢 每次切換年份後，重算 snapPoints 並置中第一張
  watch(() => props.year, () => {
    setTimeout(() => {
      snapPoints = getSnapPoints();
      centerFirstItem();
    }, 0);
  });

  onBeforeUnmount(() => {
    window.removeEventListener("resize", handleResize);
  });
});
</script>

<template>
  <div class="container m-0 p-0 position-absolute">
    <ul ref="listRef" class="item-list m-0 position-absolute d-flex list-unstyled">
      <li class="item" v-for="anime in animes" :key="anime.num">
        <img
          class="item-img img-fluid"
          :src="`/animeImages/${anime.image || '0000000000.jpg'}`"
          :alt="anime.cn"
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
  padding: 2vw;
}
.item-img {
  height: 25vh;
  max-width: 177px; /* 最大寬度限制 */
  width: auto;
  object-fit: contain;
}
</style>
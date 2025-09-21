<script setup>
import { ref, onMounted } from "vue";
import { gsap } from "gsap";
import { Draggable } from "gsap/Draggable";
import { InertiaPlugin } from "gsap/InertiaPlugin";
import { getAllYears } from '../services/gamerAcg.js'

gsap.registerPlugin(Draggable, InertiaPlugin);

const listRef = ref(null);
const containerRef = ref(null);

const animeYears = getAllYears();
const selectedNumber = ref(null); // 當前中央數字
const emit = defineEmits(["update:selected"]);

onMounted(() => {
  const ul = listRef.value;
  const items = ul.querySelectorAll(".item");
  const container = containerRef.value;

  let containerCenterY = container.getBoundingClientRect().height / 2;
  let draggable;

  function getSnapPoints() {
    return Array.from(items).map((_, i) => {
      const numberHeight = items[i].offsetHeight;
      const numberCenter = i * numberHeight + numberHeight / 2;
      return containerCenterY - numberCenter;
    });
  }

  function updateScale() {
    const ulY = draggable?.y ?? 0;
    let closestDistance = Infinity;
    let closestItem = null;

    items.forEach((item, i) => {
      const numberHeight = item.offsetHeight;
      const numberCenter = ulY + i * numberHeight + numberHeight / 2;
      const distance = Math.abs(containerCenterY - numberCenter);

      // 記錄離中央最近的數字
      if (distance < closestDistance) {
        closestDistance = distance;
        closestItem = item;
      }

      // scale 動畫
      const scale = gsap.utils.mapRange(0, numberHeight * 2, 1.5, 1)(distance);
      gsap.to(item, { scale, duration: 0.2 });
    });

    // 更新 selectedNumber
    if (closestItem) {
      selectedNumber.value = closestItem.textContent;
    }  
  }

  function initDraggable() {
    const snapPoints = getSnapPoints();
    [draggable] = Draggable.create(ul, {
      type: "y",
      edgeResistance: 0.8,
      inertia: true,
      bounds: { minY: snapPoints[snapPoints.length - 1], maxY: snapPoints[0] },
      snap: (endValue) =>
        snapPoints.reduce((prev, curr) =>
          Math.abs(curr - endValue) < Math.abs(prev - endValue) ? curr : prev
        ),
      onDrag: updateScale,
      onThrowUpdate: updateScale,
      onRelease: updateScale,
      // ✅ 慣性 + snap 完成時才觸發 emit
      onThrowComplete: () => {
        updateScale(); // 確保最後縮放正確
        if (selectedNumber.value) {
          emit("update:selected", selectedNumber.value);
        }
      }
    });
    updateScale();
  }

  initDraggable();

  window.addEventListener("resize", () => {
    containerCenterY = container.getBoundingClientRect().height / 2;
    updateScale();
  });
});
</script>

<template>
  <div class="container m-0 p-0">
    <!-- <div class="center-line"></div> -->
    <main ref="containerRef" class="content-body position-relative overflow-hidden">
      <ul ref="listRef" class="item-list list-unstyled m-0">
        <li class="item text-danger rounded" v-for="year in animeYears" :key="year">{{ year }}</li>
      </ul>
    </main>
    <div class="selected-display">
      <!-- 中央數字: {{ selectedNumber }} -->
    </div>
  </div>
</template>

<style scoped>
.container {
  position: absolute;
  transform: translate(0, -50%);
  z-index: 99;
}
.content-body {
  width: 20vw;
  height: 20vh;
}
.item {
  font-size: 3vb;
  padding: 1vh;
}
.center-line {
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  height: 2px;
  background: red;
  pointer-events: none;
  z-index: 999;
}
</style>
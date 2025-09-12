<script setup>
import { onMounted } from "vue";
import { gsap } from "gsap";
import { Draggable } from "gsap/Draggable";
import { InertiaPlugin } from "gsap/InertiaPlugin";

gsap.registerPlugin(Draggable, InertiaPlugin);

onMounted(() => {
  const ul = document.querySelector(".item-list");
  const items = ul.querySelectorAll(".item");
  const images = ul.querySelectorAll("img");

  const screenCenterX = window.innerWidth / 2;
  const cardWidth = items[0].offsetWidth;

  // 等圖片載入完成後再初始化
  let loadedCount = 0;
  images.forEach(img => {
    img.addEventListener("load", () => {
      loadedCount++;
      if (loadedCount === images.length) {
        initDraggable();
      }
    });
  });

  function getSnapPoints() {
    return Array.from(items).map((_, i) => {
      const cardCenter = i * cardWidth + cardWidth / 2;
      return screenCenterX - cardCenter;
    });
  }

  function initDraggable() {
    const snapPoints = getSnapPoints();

    Draggable.create(ul, {
      type: "x",
      edgeResistance: 0.8,
      inertia: true,
      bounds: {
        minX: snapPoints[snapPoints.length - 1],
        maxX: snapPoints[0]
      },
      snap: { x: snapPoints },
      onDrag: updateScale,
      onThrowUpdate: updateScale
    });

    // 初始化一次縮放（避免載入完成時全都同樣大小）
    updateScale.call({ target: ul, x: 0 });
  }

  function updateScale() {
    const ulX = this.x ?? 0; // this.x 可能在初始化時不存在

    items.forEach((card, i) => {
      const cardCenter = ulX + i * cardWidth + cardWidth / 2;
      const distance = Math.abs(screenCenterX - cardCenter);

      // 距離越近 → 放大
      const scale = gsap.utils.mapRange(0, 200, 1.2, 1)(distance);
      gsap.set(card, { scale });
    });
  }
});
</script>

<template>
  <div class="container m-0 p-0 vw-100 vh-100 d-fixe justify-content-center align-items-center">
    <main class="content-body position-relative overflow-hidden vw-100 vh-100">
      <ul class="item-list position-absolute d-flex bottom-0 list-unstyled bg-dark bg-opacity-10">
        <li class="item p-4"> <img class="item-img" src="../../public/animeImages/0000000000.jpg" alt="hoodie" /> </li>
        <li class="item p-4"> <img class="item-img" src="../../public/animeImages/0000000000.jpg" alt="hoodie" /> </li>
        <li class="item p-4"> <img class="item-img" src="../../public/animeImages/0000000000.jpg" alt="hoodie" /> </li>
        <li class="item p-4"> <img class="item-img" src="../../public/animeImages/0000000000.jpg" alt="hoodie" /> </li>
        <li class="item p-4"> <img class="item-img" src="../../public/animeImages/0000000000.jpg" alt="hoodie" /> </li>
        <li class="item p-4"> <img class="item-img" src="../../public/animeImages/0000000000.jpg" alt="hoodie" /> </li>
        <li class="item p-4"> <img class="item-img" src="../../public/animeImages/0000000000.jpg" alt="hoodie" /> </li>
        <li class="item p-4"> <img class="item-img" src="../../public/animeImages/0000000000.jpg" alt="hoodie" /> </li>
        <li class="item p-4"> <img class="item-img" src="../../public/animeImages/0000000000.jpg" alt="hoodie" /> </li>
        <li class="item p-4"> <img class="item-img" src="../../public/animeImages/0000145611.jpg" alt="hoodie" /> </li>
      </ul>
    </main>
  </div>
</template>

<style scoped>
.container {
  z-index: 10;
}

.item-img {
  width: 176.75px;
  height: 250px;
  object-fit: cover;
}
</style>
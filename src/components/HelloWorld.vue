<script setup>
import { onMounted } from "vue";
import { gsap } from "gsap";
import { Draggable } from "gsap/Draggable";
import { InertiaPlugin } from "gsap/InertiaPlugin";

gsap.registerPlugin(Draggable, InertiaPlugin);

onMounted(() => {
  const ul = document.querySelector(".item-list");
  const images = ul.querySelectorAll("img");
  const items = ul.querySelectorAll(".item");
  const screenCenterX = window.innerWidth / 2;
  const cardWidth = items[0].offsetWidth;

  // 等待圖片全部載入後再開始
  let loadedCount = 0;
  images.forEach(img => {
    img.addEventListener("load", () => {
      loadedCount++;
      if (loadedCount === images.length) {
        initDraggable();
      }
    });
  });

  function initDraggable() {
    const cardWidth = items[0].offsetWidth; //卡片寬度
    const snapPoints = Array.from(items).map((item, i) => {
      const cardCenter = i * cardWidth + cardWidth / 2; //卡片中心位置
      return screenCenterX - cardCenter; //回傳snap值
    });

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
  }
  
  function updateScale() {
    let ul = this.target; // 拖拉中的 ul
    let ulX = this.x;     // ul 的目前偏移量

    items.forEach((card, i) => {
      // 計算該卡片的中心點（加上 ul 偏移後）
      let cardCenter = ulX + i * cardWidth + cardWidth / 2;
      let distance = Math.abs(screenCenterX - cardCenter);

      // 距離越近 → scale 越大（這裡用簡單線性換算）
      let scale = gsap.utils.mapRange(0, 200, 1.2, 1)(distance);
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
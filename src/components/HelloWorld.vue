<!-- 參考範例：https://codepen.io/mouktardev/pen/YzVxvEv -->
<script setup>
import { onMounted } from "vue";
import { gsap } from "gsap";
import { Draggable } from "gsap/Draggable";
import { InertiaPlugin } from "gsap/InertiaPlugin";
import { Flip } from "gsap/Flip";

gsap.registerPlugin(Draggable, InertiaPlugin, Flip);

onMounted(() => {
  const items = gsap.utils.toArray(".item");
  const bgs = gsap.utils.toArray(".bg1, .bg2, .bg3");
  gsap.set([bgs[0], bgs[1]], { scale: 2, opacity: 0 });

  const panal = document.querySelector(".content-body");
  const cards = document.querySelector(".item-list");
  const spacer = document.createElement("div");
  let itemIndex;

  function activate(index) {
    if (!items[index]) return;
    let item = items[index],
      img = item.querySelector(".item-img"),
      description = item.querySelector(".item-description"),
      itemGetter = gsap.getProperty(item),
      state = Flip.getState([item, img, description], {
        props: "borderRadius,maxWidth,zIndex",
      });
    gsap.set(spacer, {
      width: itemGetter("width"),
      height: itemGetter("height"),
      marginLeft: itemGetter("marginLeft") + "px",
      marginRight: itemGetter("marginRight") + "px",
    });
    item.parentNode.insertBefore(spacer, item);
    panal.appendChild(item);
    item.classList.add("active");
    Flip.from(state, { duration: 0.5, ease: "power1.inOut", nested: true });
    itemIndex = index;
    setTimeout(() => item.addEventListener("click", deactivate), 100);
  }

  function deactivate() {
    let item = items[itemIndex],
      img = item.querySelector(".item-img"),
      description = item.querySelector(".item-description"),
      state = Flip.getState([item, img, description], {
        props: "borderRadius,maxWidth",
      });
    spacer.parentNode.insertBefore(item, spacer);
    spacer.parentNode.removeChild(spacer);
    item.classList.remove("active");
    Flip.from(state, { duration: 0.5, ease: "power1.inOut", nested: true });
    itemIndex = null;
    item.removeEventListener("click", deactivate);
  }

  Draggable.create(cards, {
    type: "x",
    edgeResistance: 0.5,
    snap: { x: [0, -360, -680] },
    zIndexBoost: false,
    onDragEnd: function () {
      let index = this.endX === 0 ? 2 : this.endX === -360 ? 1 : 0;
      gsap.to(bgs, {
        scale: (i) => (i === index ? 1 : 2),
        opacity: (i) => (i === index ? 1 : 0),
      });
    },
    onClick(e) {
      activate(items.indexOf(e.target.closest(".item")));
    },
    inertia: true,
    allowContextMenu: false,
    bounds: {
      minX: -cards.offsetWidth + panal.offsetWidth,
      maxX: 0,
    },
  });
});
</script>

<template>
  <div class="container">
    <main class="content-body">
      <div class="bacground-images">
        <div class="bg1"></div>
        <div class="bg2"></div>
        <div class="bg3"></div>
      </div>
      <header>
        <div class="menu">
          <i class="fas fa-bars"></i>
        </div>
        <div class="header-title">urban</div>
        <i class="fas fa-shopping-bag" style="font-size: 24px"></i>
      </header>
      <aside class="hero-title">
        <p>New SEASON - 020</p>
        <hr class="divider" />
        <h1>our<br />Hoodies<br />Collection</h1>
      </aside>
      <ul class="item-list">
        <li class="item" v-for="n in 6" :key="n">
          <img class="item-img" :src="`https://picsum.photos/200/200?random=${n}`" alt="hoodie" />
          <div class="item-description">
            <h1>men's hoodie {{ n }}</h1>
            <p>$ 40.00</p>
          </div>
        </li>
      </ul>
    </main>
  </div>
</template>

<style scoped>
.container {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
.content-body {
  position: fixed;   /* ← 改成 fixed */
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%); /* 永遠置中 */
  overflow: hidden;   /* 依需求保留 */
  width: 400px;
  height: 800px;
  box-shadow: rgba(0, 0, 0, 0.19) 0px 10px 20px,
              rgba(0, 0, 0, 0.23) 0px 6px 6px;
  z-index: 10;       /* 確保在背景之上 */
}

.bacground-images {
  position: absolute;
  overflow: hidden;
  z-index: -1;
  height: 100%;
  width: 100%;
}

.bg1,
.bg2,
.bg3 {
  position: absolute;
  width: 100%;
  height: 100%;
  background-repeat: no-repeat;
  background-size: cover;
}

.bg1 {
  background-image: url("https://picsum.photos/400/800?random=1");
}
.bg2 {
  background-image: url("https://picsum.photos/400/800?random=2");
}
.bg3 {
  background-image: url("https://picsum.photos/400/800?random=3");
}
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  color: white;
}
.header-title {
  font-family: "Krona One", sans-serif;
  text-transform: uppercase;
  font-size: 2rem;
  letter-spacing: 2px;
}
.hero-title {
  padding: 0 20px 20px 20px;
  margin: 40px 0 250px 0;
}
.hero-title p {
  font-family: sans-serif;
  text-transform: uppercase;
  color: white;
}
.hero-title h1 {
  font-family: "Krona One", sans-serif;
  color: white;
  font-size: 1.5rem;
  text-align: right;
}
.item-list {
  position: absolute;
  margin-left: 10px;
  display: flex;
}
.item {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  margin: 5px;
  width: 170px;
  height: 220px;
  border-radius: 10px;
  background-color: white;
}
.item.active {
  position: absolute;
  bottom: 0;
  height: 340px;
  width: 100%;
  border-radius: 0;
  margin: 0;
  z-index: 1000;
}
.item.active .item-img {
  max-width: 50%;
  bottom: 240px;
}
.item.active .item-description {
  bottom: 140px;
}
.item-img {
  position: absolute;
  align-self: center;
  display: block;
  height: auto;
  bottom: 100px;
  max-width: 100%;
}
.item-description {
  position: absolute;
  bottom: 0;
}
.item-description h1 {
  text-transform: uppercase;
  padding: 15px 15px 0 15px;
  font-size: 1rem;
}
.item-description p {
  font-family: sans-serif;
  padding: 0 15px 15px 15px;
  color: gray;
}
body {
  margin: 0 auto;
  background-color: gray;
}
li {
  list-style-type: none;
}
</style>
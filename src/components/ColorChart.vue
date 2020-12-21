<template>
  <div class="blocks-wrap">
    <div class="blocks">
      <div
        class="block"
        v-for="block in blocks"
        :key="block"
        :style="{background: block}"
      ><span>{{block}}</span></div>
    </div>
    <p><br /><br />{{blocks.length}}</p>
  </div>
</template>

<script>
export default {
  name: 'ColorChart',
  computed: {
    blocks() {
      const result = []
      const max = 256;
      const unit = 128;
      for(let r = 0; r <= max; r += unit) {
        for(let g = 0; g <= max; g += unit) {
          for(let b = 0; b <= max; b += unit) {
            result.push(`rgb(${r}, ${g}, ${b})`)
          }
        }
      }
      for(let k = 0; k <= max; k += 32) {
        result.push(`rgb(${k}, ${k}, ${k})`)
      }
      return result
    },
  },
}
</script>

<style scoped>
.blocks {
  display: flex;
  flex-wrap: wrap;
}
.block {
  width: calc(100% / 7);
  position: relative;
}
.block:not(:hover) span {
  visibility: collapse;
}
.block span {
  position: absolute;
  z-index: 10;
  left: 0;
  top: 0;
}
.block::before {
  padding-top: 100%;
  content: '';
  display: block;
}
</style>

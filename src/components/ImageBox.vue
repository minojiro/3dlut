<template>
  <div>
    <div class="image-box"
      @mousedown="mousedownFn"
      @mouseup="mouseupFn"
      @mousemove="mousemoveFn"
    >
      <svg
        ref="el"
        viewBox="0 0 150 100"
        xmlns="http://www.w3.org/2000/svg"
      >
        <rect x="1" y="1" width="300" height="200" fill="rgba(0,0,0,0.4)" />
        <circle v-for="([x, y], i) in controlPoints" :cx="x" :cy="y" r="2" fill="#f00" :key="i" />
        <circle v-for="([x, y], i) in points" :cx="x" :cy="y" r="1" fill="rgba(255,255,255,0.5)" :key="`p${i}`" />
      </svg>
      <canvas width="150" height="100" ref="cnv"></canvas>
    </div>
    <p>
      <input type="file" id="selectFile" @change="fileChange" accept=".png,.jpeg">
    </p>
    <p>
      <button @click="samplePixels">sample pixels</button>
    </p>
  </div>
</template>


<script>

const IMG_W = 150
const IMG_H = 100

const MAX_VAL = 255

export default {
  name: 'ImageBox',
  data() {
    return {
      controlPoints: [
        [10, 10],
        [140, 10],
        [10, 90],
        [140, 90],
      ],
      ctx: null,
      selectingPoint: null,
    }
  },
  computed: {
    points() {
      const points = []
      const cp = this.controlPoints
      const W_POINTS = 6
      const H_POINTS = 4
      for(let i = 0; i <= W_POINTS; i++) {
        const x1 = (cp[1][0] - cp[0][0]) * (i / W_POINTS) + cp[0][0]
        const y1 = (cp[1][1] - cp[0][1]) * (i / W_POINTS) + cp[0][1]
        const x2 = (cp[3][0] - cp[2][0]) * (i / W_POINTS) + cp[2][0]
        const y2 = (cp[3][1] - cp[2][1]) * (i / W_POINTS) + cp[2][1]
        for(let j = 0; j <= H_POINTS; j++) {
          const x = (x2 - x1) * (j / H_POINTS) + x1
          const y = (y2 - y1) * (j / H_POINTS) + y1
          points.push([x, y])
        }
      }
      return points
    },
  },
  methods: {
    getMousePos(e) {
      return {
        x: e.offsetX,
        y: e.offsetY,
      }
    },
    fileChange(e) {
      console.log(e)
      const reader = new FileReader();
      this.ctx = this.$refs.cnv.getContext('2d');
      const img = new Image();
      reader.readAsDataURL(e.target.files[0])
      img.onload = () => this.ctx.drawImage(img, 0, 0, IMG_W, IMG_H)
      reader.onload = () => img.src = reader.result
    },
    mousedownFn(e) {
      const m = this.getMousePos(e)
      const diffs = this.controlPoints.map(p =>
        Math.pow(p[0] - m.x, 2) + Math.pow(p[1] - m.y, 2)
      )
      this.selectingPoint = diffs.indexOf(Math.min(...diffs))
      e.preventDefault();
    },
    mousemoveFn(e) {
      if (this.selectingPoint === null) {
        return false
      }
      const ps = [...this.controlPoints]
      const m = this.getMousePos(e)
      ps[this.selectingPoint][0] = m.x
      ps[this.selectingPoint][1] = m.y
      this.controlPoints = ps
      e.preventDefault();
    },
    mouseupFn(e) {
      this.selectingPoint = null
      e.preventDefault();
    },
    samplePixels() {
      const rgbs = this.points.map(([x, y]) => {
        const [r, g, b] = this.ctx.getImageData(x, y, 1, 1).data
        return [
          parseFloat(r) / MAX_VAL,
          parseFloat(g) / MAX_VAL,
          parseFloat(b) / MAX_VAL,
        ]
      })
      this.$emit('setRgbs', rgbs)
    },
  },

}
</script>

<style scoped>
.image-box {
  width: 150px;
  position: relative;
}
.image-box svg {
  top: 0;
  left: 0;
  position: absolute;
}
</style>

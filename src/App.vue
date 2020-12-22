<template>
  <div id="app">
    <h1>3D LUT generator</h1>
    <ColorChart v-if="false" />

    <h2>base</h2>
    <ImageBox @setRgbs="setBaseRgbs" />

    <h2>target</h2>
    <ImageBox @setRgbs="setTargetRgbs" />

    <h2>list</h2>
    <!-- <p><button @click="addPoints">add</button></p> -->
    <p>{{ rgbPairsStr.length }}</p>
    <div class="list-wrap">
      <ul>
        <!-- <li v-for="(str,i) in rgbPairsStr" :key="i">{{str}}</li> -->
      </ul>
    </div>
    <p>
      <button
        :disabled="baseRgbs.length * targetRgbs.length === 0"
        @click="generate"
      >generate 3d lut</button>
      <a :href="dlUrl" v-if="dlUrl" ref="link" :download="dlFname">dl</a>
    </p>
  </div>
</template>

<script lang="ts">
import ImageBox from './components/ImageBox.vue'
import ColorChart from './components/ColorChart.vue'
import {generateFile} from './lut-generator.js'

export default {
  name: 'App',
  components: {
    ColorChart,
    ImageBox,
  },
  data() {
    return {
      baseRgbs: [],
      targetRgbs: [],
      dlUrl: "",
    }
  },
  computed: {
    rgbPairsStr() {
      const fn = f => Math.floor(f * 100) / 100
      return this.rgbPairs.map(p => (
        `${fn(p[0])} ${fn(p[1])} ${fn(p[2])} => ${fn(p[3])} ${fn(p[4])} ${fn(p[5])}`
      ))
    },
    dlFname() {
      const d = new Date()
      const dateStr = [
        'lut-diff',
        d.getFullYear(),
        d.getMonth() + 1,
        d.getDate(),
        d.getHours(),
        d.getMinutes(),
        d.getSeconds(),
      ].join('-')
      return `${dateStr}.CUBE`
    },
    rgbPairs() {
      return this.baseRgbs.map((b, i) => ([
        ...b,
        ...this.targetRgbs[i],
      ]))
    },
  },
  methods: {
    setBaseRgbs(baseRgbs) {
      this.baseRgbs = baseRgbs
    },
    setTargetRgbs(targetRgbs) {
      this.targetRgbs = targetRgbs
    },
    async generate() {
      this.dlUrl = ''
      const data = await generateFile(this.rgbPairs)
      const encodedData = encodeURIComponent(data)
      this.dlUrl = `data:application/octet-stream, ${encodedData}`
      setTimeout(() => {
        // this.$refs.link.click()
      },1)
    },
  }
}
</script>

<style>
h2 {
  border-bottom: 1px solid #e0e0e0;
}
.list-wrap {
  height: 100px;
  font-size: 10px;
  border: 1px solid #e0e0e0;
  overflow: scroll;
}
</style>

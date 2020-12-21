<template>
  <div id="app">
    <h1>3D LUT generator</h1>
    <ColorChart v-if="false" />

    <h2>base</h2>
    <ImageBox @setRgbs="setBaseRgbs" />

    <h2>target</h2>
    <ImageBox @setRgbs="setTargetRgbs" />

    <h2>result</h2>
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
    // outputJson() {
    //   return generateFile()
    //   // return JSON.stringify([{aa:'bb'}])
    // },
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
</style>

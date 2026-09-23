<script setup>
import { onMounted, ref, watch } from 'vue'
import { getJSON, postJSON } from '../api'
const room_id = ref(1)
const coats = ref(2)
const coverage = ref(8)
const persist = ref(true)
const tiered = ref(false)
const tiers = ref([])
const template = ref([])
const out = ref(null)
const err = ref('')
onMounted(async () => {
  const s = await getJSON('/api/settings')
  coverage.value = Number(s.coverage ?? 8)
  coats.value = Number(s.coats ?? 2)
  try {
    const t = JSON.parse(s.coverage_tiers || '[]')
    if (Array.isArray(t)) template.value = t.map(Number).filter(x => x > 0)
  } catch { template.value = [] }
})
const fillTiers = () => {
  const n = Math.max(1, Number(coats.value) || 1)
  const base = template.value.length === n ? template.value : []
  tiers.value = Array.from({ length: n }, (_, i) => base[i] ?? tiers.value[i] ?? coverage.value)
}
watch(tiered, on => { if (on) fillTiers() })
watch(coats, () => { if (tiered.value) fillTiers() })
const run = async () => {
  err.value = ''; out.value = null
  const body = { room_id: room_id.value, persist: persist.value, coats: coats.value, coverage: coverage.value }
  if (tiered.value) body.coverage_list = tiers.value.map(Number)
  try { out.value = await postJSON('/api/estimate', body) }
  catch (e) { err.value = String(e) }
}
</script>
<template><div class="page"><h1>估漆工作台</h1>
<label>房间ID <input v-model.number="room_id" /></label>
<label>遍数 <input type="number" min="1" v-model.number="coats" /></label>
<label>涂布率(m²/L) <input type="number" step="0.1" v-model.number="coverage" /></label>
<label><input type="checkbox" v-model="tiered" /> 遍次阶梯涂布率</label>
<label><input type="checkbox" v-model="persist" /> 写入记录</label>
<div v-if="tiered" class="tiers">
  <label v-for="(t, i) in tiers" :key="i">第{{ i + 1 }}遍
    <input type="number" step="0.1" min="0" v-model.number="tiers[i]" /> m²/L
  </label>
</div>
<button @click="run">估算</button>
<p v-if="err" class="err">{{ err }}</p>
<div v-if="out">
  <p>净 {{ out.net_m2 }} m² · <span class="hero-num">{{ out.liters }}</span> 升 · {{ out.coats }} 遍</p>
  <p v-if="out.coverage_list">逐遍涂布率: {{ out.coverage_list.join(' / ') }} m²/L</p>
  <p v-else>涂布率: {{ out.coverage }} m²/L</p>
  <p v-if="out.run_id">记录 #{{ out.run_id }}</p>
</div></div></template>
<style scoped>
label { display: block; margin: 0.4rem 0; }
.tiers { border: 1px dashed var(--line); padding: 0.5rem; margin: 0.5rem 0; }
.tiers input { width: 6rem; }
.err { color: #b03030; }
</style>

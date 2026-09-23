<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
const coverage = ref(8)
const coats = ref(2)
const tiers = ref([])
const msg = ref('')
const err = ref('')
const load = async () => {
  const s = await getJSON('/api/settings')
  coverage.value = Number(s.coverage ?? 8)
  coats.value = Number(s.coats ?? 2)
  try {
    const t = JSON.parse(s.coverage_tiers || '[]')
    tiers.value = Array.isArray(t) ? t.map(Number) : []
  } catch { tiers.value = [] }
}
onMounted(load)
const addTier = () => tiers.value.push(Number(coverage.value) || 8)
const dropTier = i => tiers.value.splice(i, 1)
const save = async () => {
  msg.value = ''; err.value = ''
  const list = tiers.value.map(Number)
  if (!list.length || list.some(x => !(x > 0))) { err.value = '阶梯模板至少一遍,且每遍涂布率必须为正数'; return }
  try {
    await postJSON('/api/settings', {
      coverage: String(coverage.value),
      coats: String(coats.value),
      coverage_tiers: JSON.stringify(list),
    })
    msg.value = '已保存(历史记录不受影响)'
    await load()
  } catch (e) { err.value = String(e) }
}
</script>
<template><div class="page"><h1>遮盖力参数</h1>
<label>单一涂布率(m²/L) <input type="number" step="0.1" v-model.number="coverage" /></label>
<label>默认遍数 <input type="number" min="1" v-model.number="coats" /></label>
<h2>默认阶梯模板</h2>
<p>估漆台开启阶梯时按此模板预填每遍涂布率;修改不影响已保存的记录。</p>
<div v-for="(t, i) in tiers" :key="i">
  <label>第{{ i + 1 }}遍 <input type="number" step="0.1" min="0" v-model.number="tiers[i]" /> m²/L</label>
  <button @click="dropTier(i)">删除</button>
</div>
<button @click="addTier">加一遍</button>
<button @click="save">保存</button>
<p v-if="msg">{{ msg }}</p>
<p v-if="err" class="err">{{ err }}</p></div></template>
<style scoped>
label { display: inline-block; margin: 0.3rem 0.5rem 0.3rem 0; }
button { margin-left: 0.5rem; }
.err { color: #b03030; }
</style>

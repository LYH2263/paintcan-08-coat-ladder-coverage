<script setup>
import { onMounted, ref, watch } from 'vue'
import { getJSON, postJSON } from '../api'

const room_id = ref(1)
const coats = ref(2)
const coverage = ref(8)
const useLadder = ref(false)
const ladder = ref([])
const persist = ref(true)
const out = ref(null)
const err = ref('')

onMounted(async () => {
  const s = await getJSON('/api/settings')
  coverage.value = Number(s.coverage)
  coats.value = Number(s.coats)
  if (Array.isArray(s.coverage_ladder_template) && s.coverage_ladder_template.length) {
    ladder.value = s.coverage_ladder_template.map(Number)
    coats.value = ladder.value.length
  } else {
    ladder.value = [coverage.value, coverage.value].slice(0, coats.value)
  }
})

// 阶梯长度必须始终跟随遍数，便于提交前即满足整单校验
watch([coats, useLadder], () => {
  const n = Math.max(0, Number(coats.value) || 0)
  if (ladder.value.length < n) {
    while (ladder.value.length < n) ladder.value.push(coverage.value)
  } else {
    ladder.value = ladder.value.slice(0, n)
  }
})

const run = async () => {
  err.value = ''
  out.value = null
  const body = { room_id: room_id.value, persist: persist.value, coats: coats.value }
  if (useLadder.value) {
    body.coverage_ladder = ladder.value.map(Number)
  } else {
    body.coverage = coverage.value
  }
  try {
    out.value = await postJSON('/api/estimate', body)
  } catch (e) {
    err.value = String(e.message || e)
  }
}
</script>

<template>
  <div class="page">
    <h1>估漆工作台</h1>
    <div class="form-row">
      <label>房间ID <input v-model.number="room_id" type="number" /></label>
      <label>遍数 <input v-model.number="coats" type="number" min="1" /></label>
    </div>

    <label class="toggle"><input type="checkbox" v-model="useLadder" /> 开启逐遍阶梯涂布率</label>

    <div v-if="!useLadder" class="form-row">
      <label>涂布率 m²/升 <input v-model.number="coverage" type="number" step="0.1" min="0.1" /></label>
    </div>

    <table v-else>
      <thead><tr><th>遍次</th><th>涂布率 m²/升</th><th>该遍用漆（升）</th></tr></thead>
      <tbody>
        <tr v-for="(c, i) in ladder" :key="i">
          <td>第 {{ i + 1 }} 遍</td>
          <td><input v-model.number="ladder[i]" type="number" step="0.1" min="0.1" /></td>
          <td>{{ out && out.coat_liters ? out.coat_liters[i] : '—' }}</td>
        </tr>
      </tbody>
    </table>

    <div class="form-row">
      <label><input type="checkbox" v-model="persist" /> 钉存为估算记录</label>
      <button @click="run">估算</button>
    </div>

    <p v-if="err" class="err">{{ err }}</p>
    <div v-if="out" class="result">
      <p>净 {{ out.net_m2 }} m² · 共 <span class="hero-num">{{ out.liters }}</span> 升 · {{ out.coats }} 遍</p>
      <p v-if="out.coverage_ladder">逐遍涂布率：{{ out.coverage_ladder.join(' / ') }} m²/升；逐遍升数：{{ out.coat_liters.join(' + ') }} 升</p>
      <p v-else>单一涂布率 {{ out.coverage }} m²/升 × {{ out.coats }} 遍</p>
      <p v-if="out.run_id">已钉存为记录 #{{ out.run_id }}</p>
    </div>
  </div>
</template>

<style scoped>
.form-row { display:flex; gap:1rem; align-items:center; margin:0.75rem 0; flex-wrap:wrap; }
.toggle { display:block; margin:0.75rem 0; font-weight:600; }
.err { color:#b3261e; }
.result { margin-top:1rem; border-top:1px dashed #aacce0; padding-top:0.5rem; }
</style>

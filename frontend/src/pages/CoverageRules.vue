<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'

const s = ref({})
const template = ref([])
const saved = ref(false)
const err = ref('')

onMounted(async () => {
  s.value = await getJSON('/api/settings')
  const t = s.value.coverage_ladder_template
  template.value = Array.isArray(t) && t.length ? t.map(Number) : [Number(s.value.coverage || 8), Number(s.value.coverage || 8)]
})

const addCoat = () => template.value.push(Number(s.value.coverage || 8))
const removeCoat = () => template.value = template.value.slice(0, Math.max(1, template.value.length - 1))

const save = async () => {
  saved.value = false
  err.value = ''
  try {
    const r = await postJSON('/api/settings/ladder-template', { coverage_ladder: template.value.map(Number) })
    template.value = r.coverage_ladder_template
    s.value.coverage_ladder_template = r.coverage_ladder_template
    saved.value = true
  } catch (e) {
    err.value = String(e.message || e)
  }
}
</script>

<template>
  <div class="page">
    <h1>遮盖力参数</h1>
    <p>每升可刷 {{ s.coverage }} m² · 默认 {{ s.coats }} 遍</p>

    <h2>默认阶梯涂布率模板</h2>
    <p class="hint">估漆台开启阶梯时自动套用；模板只影响新估算，已钉存的历史记录不会随之改变。</p>
    <table>
      <thead><tr><th>遍次</th><th>涂布率 m²/升</th></tr></thead>
      <tbody>
        <tr v-for="(c, i) in template" :key="i">
          <td>第 {{ i + 1 }} 遍</td>
          <td><input v-model.number="template[i]" type="number" step="0.1" min="0.1" /></td>
        </tr>
      </tbody>
    </table>
    <div class="row">
      <button @click="addCoat">加一遍</button>
      <button @click="removeCoat">减一遍</button>
      <button class="primary" @click="save">存为默认模板</button>
    </div>
    <p v-if="saved" class="ok">已保存：{{ template.join(' / ') }} m²/升</p>
    <p v-if="err" class="err">{{ err }}</p>
  </div>
</template>

<style scoped>
.row { display:flex; gap:0.75rem; margin-top:0.75rem; flex-wrap:wrap; }
.hint { color:#4a6a7a; font-size:0.9rem; }
.ok { color:#1e7a46; }
.err { color:#b3261e; }
</style>

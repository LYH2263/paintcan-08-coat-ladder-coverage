<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'

const items = ref([])
const openId = ref(null)
const detail = ref(null)
const err = ref('')

onMounted(async () => { items.value = (await getJSON('/api/history')).items })

const toggle = async (id) => {
  if (openId.value === id) { openId.value = null; detail.value = null; return }
  err.value = ''
  detail.value = null
  openId.value = id
  try {
    // 重新从库中取回该条，钉选的逐遍涂布率与升数随记录原样返回
    detail.value = await getJSON(`/api/history/${id}`)
  } catch (e) {
    err.value = String(e.message || e)
  }
}
</script>

<template>
  <div class="page">
    <h1>估算记录</h1>
    <table>
      <thead><tr><th>#</th><th>时间</th><th>升数</th><th>模式</th><th></th></tr></thead>
      <tbody>
        <tr v-for="h in items" :key="h.id">
          <td>#{{ h.id }}</td>
          <td>{{ h.created_at }}</td>
          <td>{{ (h.result && h.result.liters) ?? '—' }}</td>
          <td>{{ h.result && h.result.coverage_ladder ? '阶梯 ' + h.result.coverage_ladder.length + ' 遍' : '单一涂布率' }}</td>
          <td><button @click="toggle(h.id)">{{ openId === h.id ? '收起' : '打开' }}</button></td>
        </tr>
      </tbody>
    </table>

    <p v-if="err" class="err">{{ err }}</p>

    <div v-if="detail" class="detail">
      <h2>记录 #{{ detail.id }}</h2>
      <p>净面积 {{ detail.result.net_m2 }} m² · 合计 <span class="hero-num">{{ detail.result.liters }}</span> 升 · {{ detail.result.coats }} 遍</p>
      <template v-if="detail.result.coverage_ladder">
        <p>该条钉选的逐遍涂布率（模板后续修改不影响本条）：</p>
        <table>
          <thead><tr><th>遍次</th><th>涂布率 m²/升</th><th>用漆（升）</th></tr></thead>
          <tbody>
            <tr v-for="(c, i) in detail.result.coverage_ladder" :key="i">
              <td>第 {{ i + 1 }} 遍</td>
              <td>{{ c }}</td>
              <td>{{ detail.result.coat_liters ? detail.result.coat_liters[i] : '—' }}</td>
            </tr>
          </tbody>
        </table>
      </template>
      <p v-else>单一涂布率 {{ detail.result.coverage }} m²/升 × {{ detail.result.coats }} 遍</p>
    </div>
  </div>
</template>

<style scoped>
.detail { margin-top:1rem; border-top:2px dashed #aacce0; padding-top:0.75rem; }
.err { color:#b3261e; }
</style>

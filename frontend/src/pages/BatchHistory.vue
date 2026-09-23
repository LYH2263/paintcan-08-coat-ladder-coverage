<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
const openId = ref(null)
const parse = s => { try { return JSON.parse(s) } catch { return {} } }
const toggle = h => { openId.value = openId.value === h.id ? null : h.id }
onMounted(async () => { items.value = (await getJSON('/api/history')).items })
</script>
<template><div class="page"><h1>估算记录</h1><table>
<tr><th>#</th><th>时间</th><th>房间</th><th>升数</th></tr>
<template v-for="h in items" :key="h.id">
  <tr @click="toggle(h)" class="row">
    <td>#{{ h.id }}</td><td>{{ h.created_at }}</td><td>{{ h.room_id }}</td>
    <td>{{ parse(h.result_json).liters }}</td>
  </tr>
  <tr v-if="openId === h.id"><td colspan="4">
    <p>净面积 {{ parse(h.result_json).net_m2 }} m² · {{ parse(h.result_json).coats ?? parse(h.input_json).coats }} 遍 · 合计 {{ parse(h.result_json).liters }} 升</p>
    <p v-if="parse(h.result_json).coverage_list">
      钉选逐遍涂布率: {{ parse(h.result_json).coverage_list.join(' / ') }} m²/L
    </p>
    <p v-else>涂布率: {{ parse(h.input_json).coverage }} m²/L × {{ parse(h.input_json).coats }} 遍</p>
  </td></tr>
</template>
</table></div></template>
<style scoped>
.row { cursor: pointer; }
.row:hover { background: #eef7fc; }
</style>

<template>
  <div class="node-library">
    <h3 class="title">🧩 轮函数组件库</h3>

    <el-collapse v-model="activePanels" accordion>
      <!-- 输入 -->
      <el-collapse-item title="输入变量" name="input">
        <div class="items">
          <NodeItem
            v-for="item in categorized.input"
            :key="item.type"
            :item="item"
            @select="onAdd(item)"
          />
        </div>
      </el-collapse-item>

      <!-- 密钥 -->
      <el-collapse-item title="密钥组件" name="key">
        <div class="items">
          <NodeItem
            v-for="item in categorized.key"
            :key="item.type"
            :item="item"
            @select="onAdd(item)"
          />
        </div>
      </el-collapse-item>

      <!-- 线性 -->
      <el-collapse-item title="线性组件" name="linear">
        <div class="items">
          <NodeItem
            v-for="item in categorized.linear"
            :key="item.type"
            :item="item"
            @select="onAdd(item)"
          />
        </div>
      </el-collapse-item>

      <!-- 非线性 -->
      <el-collapse-item title="非线性组件" name="nonlinear">
        <div class="items">
          <NodeItem
            v-for="item in categorized.nonlinear"
            :key="item.type"
            :item="item"
            @select="onAdd(item)"
          />
        </div>
      </el-collapse-item>

      <!-- 常量 -->
      <el-collapse-item title="常量组件" name="constant">
        <div class="items">
          <NodeItem
            v-for="item in categorized.constant"
            :key="item.type"
            :item="item"
            @select="onAdd(item)"
          />
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineComponent, h, type PropType } from 'vue'
import { nodeRegistry } from '@/config/NodeRegistry'
import type { NodeConfig } from '@/config/NodeRegistry'
import { useNodeStore } from '@/stores/useNodeStore'
import { nanoid } from 'nanoid'

const store = useNodeStore()
const activePanels = ref<string[]>(['input'])

/**
 * NodeItem 渲染条目
 */
const NodeItem = defineComponent({
  name: 'NodeItem',
  props: {
    item: {
      type: Object as PropType<NodeConfig>,
      required: true
    }
  },
  emits: ['select'],
  setup(props, { emit }) {
    const handleClick = () => emit('select', props.item)
    return () =>
      h('div', { class: 'lib-item', onClick: handleClick }, [
        props.item.icon ? h('img', { src: props.item.icon, class: 'icon' }) : null,
        h('div', { class: 'info' }, [
          h('span', { class: 'label' }, props.item.label),
          props.item.desc ? h('span', { class: 'desc' }, props.item.desc) : null
        ])
      ])
  }
})

/**
 * Pinia 适配版新增节点
 * --------------------------------------------------------
 * 完全符合 useNodeStore 中 CanvasNode 的结构
 */
function onAdd(cfg: NodeConfig) {
  const id = nanoid()

  store.addNode({
    id,
    type: cfg.type,                     // 必须与 VueFlow & store 的注册类型一致
    position: { x: 100, y: 100 },       // 默认位置
    data: {
      label: cfg.label,                 // 展示名称
      props: store.getDefaultProps(cfg.type) // 根据 nodeRegistry.schema 自动生成默认 props
    }
  })
}

/**
 * 分类映射
 */
const CATEGORY_MAP = {
  input: ['plainVar'],
  key: ['keyVar'],
  linear: ['xor', 'rotate'],
  nonlinear: ['sbox', 'modadd'],
  constant: ['constant']
}

const categorized = computed(() => {
  const result: Record<string, NodeConfig[]> = {}
  for (const [cat, types] of Object.entries(CATEGORY_MAP)) {
    result[cat] = nodeRegistry.filter(n => types.includes(n.type))
  }
  return result
})
</script>

<style scoped>
.node-library {
  padding: 16px;
  background: #fafafa;
  border-right: 1px solid #e5e5e5;
  height: 100%;
  overflow-y: auto;
  box-sizing: border-box;
}

.title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #333;
}

.items {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 6px 0;
}

.lib-item {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 10px;
  padding: 10px 12px;
  cursor: pointer;
  transition: all 0.25s ease;
}

.lib-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  border-color: #409eff;
}

.icon {
  width: 26px;
  height: 26px;
}

.info {
  display: flex;
  flex-direction: column;
}

.label {
  font-weight: 500;
  color: #222;
  font-size: 14px;
}

.desc {
  font-size: 12px;
  color: #888;
  margin-top: 2px;
}
</style>

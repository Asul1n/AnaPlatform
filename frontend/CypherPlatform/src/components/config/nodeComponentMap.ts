import { nodeRegistry } from './NodeRegistry'
import { markRaw } from 'vue'

// 动态导入 ../Nodes 目录下所有 .vue 文件
const nodeModules = import.meta.glob('../Nodes/**/*.vue', { eager: true })

export const nodeComponentMap = Object.fromEntries(
  nodeRegistry.map(node => {
    const vueName = node.vueRender + '.vue'

    // 尝试匹配完整文件路径
    const match = Object.entries(nodeModules).find(([path]) =>
      path.endsWith('/' + vueName)
    )

    if (!match) {
      console.warn(`⚠️ 未找到节点组件: ${vueName}`)
      return [node.type, null]
    }

    const [, mod] = match
    return [node.type, markRaw((mod as any).default)]
  })
)

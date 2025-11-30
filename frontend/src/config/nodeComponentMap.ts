import { nodeRegistry } from './NodeRegistry'
import { markRaw } from 'vue'

const modules = import.meta.glob('../components/Nodes/**/*.vue', { eager: true })

export const nodeComponentMap = Object.fromEntries(
  nodeRegistry.map(node => {
    const vueName = node.vueRender + '.vue'

    // 找出匹配的组件文件
    const match = Object.entries(modules).find(([path]) =>
      path.endsWith('/' + vueName)
    )

    if (!match) {
      console.warn(`❗未找到节点组件: ${vueName}`)
      return [node.type, null]
    }

    const [, mod] = match
    return [node.type, markRaw((mod as any).default)]
  })
)

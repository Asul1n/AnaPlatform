// composables/useExportGraph.ts
import { computed } from "vue"
import { useNodeStore } from "@/stores/useNodeStore"
import { useEdgeStore } from "@/stores/useEdgeStore"
import { useAnalysisStore } from "@/stores/useAnalysisStore"
import {
    generatePorts,
    resolvePortName,
    type PortConfig
} from "@/config/portNaming"

export function useExportGraph() {
    const nodeStore = useNodeStore()
    const edgeStore = useEdgeStore()
    const analysisStore = useAnalysisStore()

    // ----------- 1. 每个节点的端口配置（永远返回 PortConfig）-----------
    const nodePortMap = computed<Record<string, PortConfig>>(() => {
        const map: Record<string, PortConfig> = {}
        nodeStore.nodes.forEach(node => {
            map[node.id] = generatePorts(node) ?? { inputs: [], outputs: [] }
        })
        return map
    })

    // ----------- 2. 节点名字映射：支持 plainVar/keyVar + 大写前缀自动编号 -----------
    const nodeNameMap = computed<Record<string, string>>(() => {
        const map: Record<string, string> = {}
        const typeCount: Record<string, number> = {}

        nodeStore.nodes.forEach(node => {
            const isDirectNameNode =
                node.type === "plainVar" || node.type === "keyVar"

            if (isDirectNameNode) {
                // 输入 / 密钥：使用 props.name 优先
                map[node.id] =
                    node.data?.props?.name ||
                    node.data?.label ||
                    node.type.toUpperCase() ||
                    `NODE_${node.id.slice(0, 6)}`
                return
            }

            // 普通节点：按类型计数（大写前缀 + 序号）
            const base = node.type.toUpperCase()

            if (!typeCount[base]) typeCount[base] = 0
            typeCount[base]++

            map[node.id] = `${base}${typeCount[base]}`
        })

        return map
    })

    // ----------- 3. 构建边（确保 resolvePortName 不会收到 undefined）-----------
    function buildEdges() {
        const edges = edgeStore.edges
        const names = nodeNameMap.value
        const ports = nodePortMap.value

        return edges.map(e => {
            const srcNode = nodeStore.nodes.find(n => n.id === e.source)!
            const tgtNode = nodeStore.nodes.find(n => n.id === e.target)!

            const srcPortConfig = ports[srcNode.id]
            const tgtPortConfig = ports[tgtNode.id]

            const srcPort = resolvePortName(
                srcNode,
                (e as any).sourceHandle,
                srcPortConfig,
                true
            )

            const tgtPort = resolvePortName(
                tgtNode,
                (e as any).targetHandle,
                tgtPortConfig,
                false
            )

            return {
                source: srcPort
                    ? `${names[srcNode.id]}_${srcPort}`
                    : names[srcNode.id],

                target: tgtPort
                    ? `${names[tgtNode.id]}_${tgtPort}`
                    : names[tgtNode.id]
            }
        })
    }

    // ----------- 4. 最终导出结构 -----------
    function exportGraph() {

        const nodes = nodeStore.nodes.map(n => {
            // 提取基础数据
            const baseNode = {
                id: n.id,
                name: nodeNameMap.value[n.id],
                type: n.type,
                ports: nodePortMap.value[n.id],
                // 预设一个空的 props 对象，后面根据类型添加具体属性
                props: {} as Record<string, any>
            }

            // 1. 处理 plainVar 和 keyVar 的位宽属性
            if (n.type === "plainVar" || n.type === "keyVar") {
                // 假设 bitwidth 存储在 n.data.props.bitwidth 中
                const props = n.data.props as {name?: string, bitwidth?: number, mode?: string}
                const bitwidthValue = props.bitwidth

                if (bitwidthValue !== undefined) {
                    baseNode.props.bitwidth = bitwidthValue
                }
            }

            // 2. 处理 Rotate 组件的偏移量属性
            if (n.type === "rotate") {
                // 假设 offset 存储在 n.data.props.offset 中
                const props = n.data.props as {direction?: string, offset?:number, bitwidth?: number}
                const offsetValue = props.offset
                if (offsetValue !== undefined) {
                    baseNode.props = props
                }
            }
            
            // 如果 props 为空，可以选择不导出 props 字段，或保留它
            if (Object.keys(baseNode.props).length === 0) {
                delete baseNode.props
            }

            return baseNode
        })


        const edges = buildEdges()

        const basicParams = analysisStore.exportConfig()

        return {
            basicParams,
            nodes,
            edges
        }
    }

    return {
        exportGraph,
        nodePortMap,
        nodeNameMap
    }
}

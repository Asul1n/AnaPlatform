// composables/useExportGraph.ts
import { computed } from "vue"
import { useNodeStore } from "@/stores/useNodeStore"
import { useVueFlow } from "@vue-flow/core"
import {
    generatePorts,
    resolvePortName,
    type PortConfig
} from "@/config/portNaming"

export function useExportGraph() {
    const nodeStore = useNodeStore()
    const { getEdges } = useVueFlow()

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
        const edges = getEdges.value
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
        const nodes = nodeStore.nodes.map(n => ({
            id: n.id,
            name: nodeNameMap.value[n.id],
            type: n.type,
            ports: nodePortMap.value[n.id]
        }))

        const edges = buildEdges()

        return {
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

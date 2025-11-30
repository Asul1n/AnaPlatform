// src/utils/portNaming.ts

// ▶ 特殊组件（无输入/输出端口）
const SPECIAL_NODE_TYPES = new Set(["plainVar", "keyVar","constant"])

export interface PortConfig {
    inputs: string[]
    outputs: string[]
}

/**
 * 为每个节点生成端口命名
 * @param node 节点（来自 nodeStore）
 */
export function generatePorts(node: any): PortConfig {
    const type = node.type

    // ---- 特殊节点：不需要端口命名，直接返回空 ----
    if (SPECIAL_NODE_TYPES.has(type)) {
        return { inputs: [], outputs: [] }
    }

    const inputs  = node.data.ports?.inputs || []
    const outputs = node.data.ports?.outputs || []

    // ---- 遵循统一规范：input1 / output3 等 ----
    const makeIn = (i: number) => `input${i + 1}`
    const makeOut = (i: number) => `output${i + 1}`

    return {
        inputs: inputs.map((_: any, i: number) => makeIn(i)),
        outputs: outputs.map((_: any, i: number) => makeOut(i)),
    }
}

/**
 * 解析 VueFlow handle 为新的端口名
 */
export function resolvePortName(
    node: any,
    rawHandle: string | null | undefined,
    portMap: PortConfig,
    isSource: boolean
): string | undefined {
    const oldPorts = isSource ? node.data.ports.outputs : node.data.ports.inputs
    const newPorts = isSource ? portMap.outputs : portMap.inputs

    // 特殊节点 → 不需要端口
    if (SPECIAL_NODE_TYPES.has(node.type)) return undefined

    // 无 handle → 如果单端口则直给
    if (!rawHandle) return newPorts.length === 1 ? newPorts[0] : undefined

    // 旧端口名直接匹配
    let idx = oldPorts.indexOf(rawHandle)
    if (idx !== -1) return newPorts[idx]

    // handle 前缀带 nodeId
    const stripped = rawHandle.replace(new RegExp(`^${node.id}[-_.:]?`), "")
    idx = oldPorts.indexOf(stripped)
    if (idx !== -1) return newPorts[idx]

    // fallback
    return newPorts.length === 1 ? newPorts[0] : undefined
}

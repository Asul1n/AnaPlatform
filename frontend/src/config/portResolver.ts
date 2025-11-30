// portResolver.ts
import { nodePortSchema, type PortSpec, type PortPattern, type PortAlias, type PortFactory } from "@/config/nodePortSchema"

function padNumber(n: number, width?: number) {
  if (!width || width <= 0) return String(n)
  return String(n).padStart(width, '0')
}

function expandSpec(spec: PortSpec, props?: Record<string, any>, seenAliases = new Set<string>()): string[] {
  if (!spec) return []
  if (Array.isArray(spec)) {
    return spec.flatMap(s => expandSpec(s as PortSpec, props, seenAliases))
  }

  if (typeof spec === 'function') {
    // factory
    const result = (spec as PortFactory)(props)
    return [...(result.inputs ?? []), ...(result.outputs ?? [])] // not ideal, but factory used differently below
  }

  if (typeof spec === 'string') {
    // a fixed name
    return [spec]
  }

  // object cases
  if ((spec as PortPattern).pattern && (spec as PortPattern).count !== undefined) {
    const p = spec as PortPattern
    const start = p.startIndex ?? 1
    const pad = p.pad ?? 0
    const arr: string[] = []
    for (let i = 0; i < p.count; i++) {
      arr.push(`${p.pattern}${padNumber(start + i, pad)}`)
    }
    return arr
  }

  if ((spec as PortAlias).aliasOf) {
    const alias = (spec as PortAlias).aliasOf
    if (seenAliases.has(alias)) return [] // 避免循环 alias
    seenAliases.add(alias)
    const aliased = nodePortSchema[alias]
    if (!aliased) return []
    // aliased 可以是函数或 object
    if (typeof aliased === 'function') {
      const expanded = (aliased as any)(props)
      return [...expandSpec(expanded.inputs ?? [], props, seenAliases), ...expandSpec(expanded.outputs ?? [], props, seenAliases)]
    } else {
      return [...expandSpec((aliased as any).inputs ?? [], props, seenAliases), ...expandSpec((aliased as any).outputs ?? [], props, seenAliases)]
    }
  }

  return []
}

/**
 * 返回 { inputs: [], outputs: [] }
 */
export function resolvePorts(type: string, props?: Record<string, any>) {
  const entry = nodePortSchema[type]
  if (!entry) {
    // fallback: 最少生成 input1 & output1
    return { inputs: ['input1'], outputs: ['output1'] }
  }

  let item = entry
  if (typeof entry === 'function') {
    item = (entry as Function)(props)
  }

  const inputs: string[] = []
  const outputs: string[] = []

  const pushExpanded = (spec: PortSpec | PortSpec[] | undefined, arr: string[]) => {
    if (!spec) return
    if (Array.isArray(spec)) {
      for (const s of spec) arr.push(...expandSpec(s, props))
    } else {
      arr.push(...expandSpec(spec as PortSpec, props))
    }
  }

  pushExpanded((item as any).inputs, inputs)
  pushExpanded((item as any).outputs, outputs)

  // 去重并保留顺序
  const uniq = (a: string[]) => Array.from(new Set(a))
  return { inputs: uniq(inputs), outputs: uniq(outputs) }
}

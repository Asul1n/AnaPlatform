/* 定义各类的面板接口 */

export interface ShiftProps {
  direction: string
  offset: number
  bitwidth: number
}

export interface SBoxProps {
  sboxId: number
  sboxBit: number
  sboxTable: number[]
}

export interface PlainVarProps {
  name: string
  bitwidth: number
  mode: 'input' | 'output'
}

export interface KeyVarProps {
  name: string
  bitwidth: number
}


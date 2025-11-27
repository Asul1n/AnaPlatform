/* 定义各类的面板接口 */

export interface ShiftProps {
  direction: string
  shift: number
  width: number
}

export interface SBoxProps {
  sboxId: number
  sboxBit: number
  sboxTable: number[]
}

export interface PlainVarProps {
  name: string
  width: number
  mode: 'input' | 'output'
}

export interface KeyVarProps {
  name: string
  width: number
}

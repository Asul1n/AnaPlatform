// src/composables/useBasicParamsForm.ts

import { reactive, ref } from 'vue';
import type { ElForm, FormRules } from 'element-plus';
import { useAnalysisStore, type BasicAlgorithmParams } from '@/stores/useAnalysisStore'; 

// 本地表单状态接口，与 Pinia Store 的 BasicAlgorithmParams 保持一致
type BasicParamsLocal = BasicAlgorithmParams;

/**
 * 组合式函数：用于管理分组算法基本参数的表单逻辑
 */
export function useBasicParamsForm() {
  const store = useAnalysisStore();
  const formRef = ref<InstanceType<typeof ElForm> | null>(null);

  // 1. 本地拷贝 (local): 从 Store 中获取当前值作为本地状态的初始化值
  const local = reactive<BasicParamsLocal>({
    algorithmName: store.basicParams.algorithmName,
    blockSize: store.basicParams.blockSize,
    branchNum: store.basicParams.branchNum,
    roundFunction: store.basicParams.roundFunction,
    roundNum: store.basicParams.roundNum,
    note: store.basicParams.note,
  });

  // 2. 校验规则 (rules)
  const rules: FormRules = {
    algorithmName: [
      { required: true, message: '请输入算法名称', trigger: 'blur' },
      { min: 2, message: '算法名称过短', trigger: 'blur' },
    ],
    blockSize: [
      { required: true, message: '请输入分组长度', trigger: 'blur' },
      {
        validator: (_: any, value: number) => {
          if (!Number.isInteger(value) || value <= 0) {
            return new Error('分组长度必须为正整数');
          }
          return true;
        },
        trigger: 'blur',
      },
    ],
    branches: [
      { required: true, message: '请输入分支数', trigger: 'blur' },
      {
        validator: (_: any, value: number) => {
          if (!Number.isInteger(value) || value <= 0) {
            return new Error('分支数必须为正整数');
          }
          return true;
        },
        trigger: 'blur',
      },
    ],
    roundFunction: [
      { required: true, message: '请描述轮函数', trigger: 'blur' },
      { min: 3, message: '轮函数描述过短', trigger: 'blur' },
    ],
    rounds: [
      {
        validator: (_: any, value: number) => {
          if (value == null) return true;
          if (!Number.isInteger(value) || value < 0) {
            return new Error('轮数须为非负整数');
          }
          return true;
        },
        trigger: 'blur',
      },
    ],
  };

  // 3. 同步到 Pinia store (实时同步)
  function syncToStore() {
    // 使用 Object.assign 确保所有字段都被更新，且保持响应性
    Object.assign(store.basicParams, local);
  }

  // 4. 重置 (从 Store 恢复到当前持久化状态)
  function onReset() {
    // 从 store 恢复 local 状态
    Object.assign(local, store.basicParams);
  }

  // 5. 示例填充
  function fillExample() {
    Object.assign(local, {
      algorithmName: 'Feistel-DES',
      blockSize: 64,
      branchNum: 2, // Feistel通常为2
      roundFunction: 'F(R, K) = S(R ⊕ K) P',
      roundNum: 16,
      note: 'DES 结构示例',
    });
    syncToStore(); // 填充后立即同步到全局
  }

  // 确保在 setup 阶段结束后，Store 状态被正确加载到本地（如果 Store 有初始值或从本地存储加载）
  // 实际上，由于 local 已经从 store 初始化，这一步不是必须的，但作为收尾步骤保持syncToStore调用也是可以的。
  
  return {
    formRef,
    local,
    rules,
    syncToStore,
    onReset,
    fillExample,
    store, // 暴露 store 方便组件中调用 store.submitToBackend()
  };
}
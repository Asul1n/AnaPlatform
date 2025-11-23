<script setup>
import { ref } from 'vue'
import axios from 'axios'

const username = ref('')
const password = ref('')
const message  = ref('')

async function login() {
  const res = await axios.post('http://127.0.0.1:8000/api/login',{
    username: username.value,
    password: password.value,
  })
  if (res.data.success) {
    message.value = `欢迎回啦，${res.data.name}`
  } else {
    message.value = res.data.msg
  }
}
</script>

<template>
  <div>
    <h2>登录</h2>
    <input v-model="username" placeholder="用户名">
    <input v-model="password" type="password" placeholder="密码">
    <button @click="login">登录</button>
    <p>{{ message }}</p>
  </div>
</template>

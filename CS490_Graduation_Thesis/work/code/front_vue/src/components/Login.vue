<template>
  <!-- loginButton -->
  <el-button
      round
      plain
      type="primary"
      class="loginButton"
      v-if="!loginCondition"
      @click="loginPageVisible = true">
    login
  </el-button>
  <!-- loginPage -->
  <el-dialog
      align-center
      class="loginPage"
      title="Login Page"
      :show-close="false"
      v-model="loginPageVisible">
    <div class="loginPageInputs">
      <input v-model="username" class="username" placeholder="username"><br>
      <input v-model="password" class="password" type="password" placeholder="password"><br>
    </div>
    <div class="loginPageButtons">
      <el-button class="confirm" type="primary" @click="handleLogin">Login</el-button>
      <el-button @click="loginPageVisible = false">Cancel</el-button>
    </div>
  </el-dialog>
  <!-- homeDropdown -->
  <el-dropdown
      trigger="click"
      class="homeDropdown"
      placement="bottom-end">
    <el-button
        round
        plain
        type="primary"
        class="homeButton"
        v-if="loginCondition">
      home
    </el-button>
    <template #dropdown>
      <el-dropdown-menu class="homeMenu">
        <el-dropdown-item class="Information">
          <i class="ri-account-circle-line"></i>
          information
        </el-dropdown-item>
        <el-dropdown-item class="Setting">
          <i class="ri-settings-2-line"></i>
          setting
        </el-dropdown-item>
        <el-dropdown-item class="Exit" divided @click="loginCondition = false">
          <i class="ri-logout-box-r-line"></i>
          exit
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup>
import {ref} from 'vue'
// 可见性判断
const loginPageVisible = ref(false) // login界面
const loginCondition = ref(false) // 登录状态
// 用户名密码
const username = ref('')
const password = ref('')

// 登录操作
async function handleLogin() {
  // 这里可以处理用户名和密码，例如发送到服务器验证
  console.log('Username:', username.value)
  console.log('Password:', password.value)
  if (username.value !== '' && password.value !== '') {
    try {
      //TODO: 登录验证
      // 发送请求
      // const response = await axios.post('https://your-api-endpoint/login', {
      //   username: username.value,
      //   password: password.value,
      // });
      const response = {data: {success: true}}
      if (response.data.success) {
        console.log('response:', response.data.success)
        // 关闭弹窗
        loginPageVisible.value = false
        loginCondition.value = true
      } else {
        alert('Login failed: ' + response.data.message);
      }
    } catch (error) {
      console.error('Error during login:', error);
      alert('An error occurred during login.');
    }
  } else {
    alert('Please enter a valid username or password.')
  }
}
</script>

<style>
.loginButton {
  position: fixed;
  top: 2%;
  right: 1%;
}

.loginPage {
  width: 30%;
  height: 45%;
  margin: 0 auto;
  justify-content: center;
  text-align: center;
}

.loginPageInputs input {
  width: 70%;
  padding: 10px;
  margin: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.loginPageButtons {
  padding: 10px;
  text-align: center;
}

.loginPageButtons .confirm {
  margin-right: 30px;
}

.homeButton {
  position: fixed;
  top: 2%;
  right: 1%;
}
</style>

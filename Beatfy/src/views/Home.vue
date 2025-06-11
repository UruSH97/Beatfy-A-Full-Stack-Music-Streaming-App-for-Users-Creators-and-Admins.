<template>
    <div
    style="display: flex; justify-content: center; align-items: center; min-height: 100vh; background-color: #F7E5DA; backdrop-filter: blur(10px); background-size: cover; background-position: center; flex-direction: column;">
  <div class="card">
    <h1>Experience Beatify's Musical World</h1>

    <div class="buttonn-container">
      <router-link to="/user-register" class="button">User Registration</router-link>
      <router-link to="/admin-login" class="button">Admin Login</router-link>
      <router-link to="/creator-login" class="button">Creator Login</router-link>
    </div>

    <router-link to="/user-login" class="login-link">Already have an account? Login</router-link>
  </div>
  </div>
</template>

<script>
export default {

}
</script>

<style scoped>
.card {
  border: 2px solid #832B00;
  border-radius: 10px;
  box-shadow: 0 0 20px #832B00;
  background: rgba(255, 255, 255, 0.8);
  text-align: center;
  padding: 50px;
  max-width: 800px;
  width: 100%;
  box-sizing: border-box;
}

h1 {
  margin-bottom: 20px;
  color: #832B00;
}

.buttonn-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 20px;
}

.button {
  padding: 15px;
  text-decoration: none;
  color: #fff;
  border-radius: 5px;
  background-color: #832B00;
  transition: background-color 0.3s, color 0.3s;
  cursor: pointer;
}

.button:hover {
  background-color: #fff;
  color: #832B00;
}

.login-link {
  color: #832B00;
  text-decoration: none;
  margin-top: 15px;
  display: block;
}
</style>

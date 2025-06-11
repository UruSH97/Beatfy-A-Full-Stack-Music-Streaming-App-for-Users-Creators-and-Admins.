<template>
  <div
    style="display: flex; justify-content: center; align-items: center; min-height: 100vh; background-color: #F7E5DA; backdrop-filter: blur(10px); background-size: cover; background-position: center; flex-direction: column;">
    <div
      style="width: 350px; background-color: #832B00; border-radius: 10px; padding: 30px; box-shadow: 0 0 10px rgba(0, 0, 0, .2);">
      <form @submit.prevent="register" style="display: flex; flex-direction: column;">
        <h1 style="text-align: center; color: #F7E5DA;">User Registration</h1>
        <input type="text" v-model="username" placeholder="Username"
          style="margin-bottom: 10px; border-radius: 5px; padding: 10px;" required>
        <input type="email" v-model="email" placeholder="Email"
          style="margin-bottom: 10px; border-radius: 5px; padding: 10px;" required>
        <input type="password" v-model="password" placeholder="Password"
          style="margin-bottom: 10px; border-radius: 5px; padding: 10px;" required>
        <button type="submit"
          style="margin-bottom: 10px; border-radius: 5px; padding: 10px;background-color: #F7E5DA; color: #000000; cursor: pointer;">Sign-up</button>
        <div style="text-align: center; margin-top: 10px;">
          <p style="color: #F7E5DA;">Already have an account? <router-link to="/user-login"
              style="color: #ff8940;">Login</router-link></p>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
    };
  },
  methods: {
    async register() {
      // try {
      const url = `http://127.0.0.1:5000/api/user-register`;
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: this.username,
          email: this.email,
          password: this.password,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        this.$router.push({ name: 'user-login' });
        alert(data.message);
      } else {
        alert(data.message);
        this.$router.push({ name: 'home' });
      }
      // } catch (error) {
      //   alert("An error occurred during signup", error);
      //   this.$router.push({ name: 'home' });
      // }
    },
  }
};
</script>

<template>
  <div
    style="display: flex; justify-content: center; align-items: center; min-height: 100vh; background-color: #F7E5DA; backdrop-filter: blur(10px); background-size: cover; background-position: center; flex-direction: column;">
    <div
      style="width: 300px; background-color: #832B00; border-radius: 10px; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, .2);">
      <form @submit.prevent="login" style="display: flex; flex-direction: column;">
        <h1 style="text-align: center; color: #F7E5DA">Creator Login</h1>
        <input type="email" v-model="email" placeholder="email"
          style="margin-bottom: 10px; padding: 10px; border-radius: 5px;" required>
        <input type="password" v-model="password" placeholder="Password"
          style="margin-bottom: 10px; padding: 10px; border-radius: 5px;" required>
        <button type="submit"
          style="padding: 10px; border: none; border-radius: 5px; background-color: #F7E5DA; color: #832B00; cursor: pointer;">Login</button>
        <div style="text-align: center; margin-top: 10px;">
          <p style="color: #F7E5DA;">Don't have an account? <router-link to="/user-register"
              style="color: #ff8940;">Sign-up</router-link></p>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    async login() {
        // try {
          const url = `http://127.0.0.1:5000/api/creator-login`;
          const response = await fetch(url, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              email: this.email,
              password: this.password,
            }),
          });
  
          const data = await response.json();
          if (response.ok) {
            localStorage.setItem(`creator_token`, data.token);
            alert(data.message)
            this.$router.push({ name: 'creator-dashboard'});
          } else {
            alert(data.message);
            this.$router.push({ name: 'creator-login'});
          }
        // } catch (error) {
        //   alert("An error occurred during login", error);
        //   this.$router.push({ name: 'home' });
        // }
      },
  }
};
</script>

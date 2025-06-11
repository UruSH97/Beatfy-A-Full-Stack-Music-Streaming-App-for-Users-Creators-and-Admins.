<template>
  <div>
    <div class="navbar">
      <router-link to="/admin-dashboard">
        <h1 class="fw-bold"><i class="bi bi-google-play"></i> Beatfy | Admin </h1>
      </router-link>
      <div>
        <router-link to="/manage">Manage</router-link>
        <span @click="logout" style="cursor: pointer;">Logout</span>
      </div>
    </div>


    <div class="content">

      <div class="uploads-section" style="width: 400px;">
        <div class="Admin">
          <h2>Statistics</h2>
          <div class="app-subcontainer fw-bold">Total Albums:<span>{{ details.albums }}</span></div>
          <div class="app-subcontainer fw-bold">Total Songs:<span>{{ details.songs }}</span></div>
          <div class="app-subcontainer fw-bold">Total Users:<span>{{ details.users }}</span></div>
          <div class="app-subcontainer fw-bold">Total Creators:<span>{{ details.creators }}</span></div>
          <div class="app-subcontainer fw-bold">Total Playlists:<span>{{ details.playlists }}</span></div>
        </div>
      </div>

      <div class="uploads-section">
        <div class="Admin">
          <h2>Top Songs</h2>
          <span v-for="song in top_songs">
            <div class="app-subcontainer fw-bold" >{{ song.name }}
              <span><i class="bi bi-star-fill"></i> {{ song.rating }}</span></div>
          </span>
        </div>
      </div>

      <div class="uploads-section">
        <h2>Creators</h2>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in creators" :key="c.id">
              <td>{{ c.username }}</td>
              <td style="width: 100px;">
                <span v-if="c.is_blocked">
                  <button @click="chnageStatus(c.id)">Blocked</button>
                </span>
                <span v-else>
                  <button @click="chnageStatus(c.id)">Normal</button>
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      top_songs: [],
      creators: [],
      details: {}
    };
  },
  methods: {
    async chnageStatus(Id) {
      const response = await fetch(`http://127.0.0.1:5000/api/creator/${Id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem(`admin_token`)
        },
      });
      const data = await response.json();
      if (response.ok) {
        alert(data.message);
        this.fetchCreators();
      } else {
        alert(data.message);
        this.fetchCreators();
      }
    },

    async fetchData() {
      const url = `http://127.0.0.1:5000/api/details`;
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          'Authorization': 'Bearer ' + localStorage.getItem(`admin_token`),
        },
      });
      const data = await response.json();
      if (response.ok) {
        this.details = data.details;
        this.top_songs = data.details.top_songs;
      } else {
        alert(data.message);
        // this.$router.push({ name: "login", params: { role: 'user' } });
      }
    },
    async fetchCreators() {
      const url = `http://127.0.0.1:5000/api/creator`;
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          'Authorization': 'Bearer ' + localStorage.getItem(`admin_token`),
        },
      });
      const data = await response.json();
      if (response.ok) {
        this.creators = data.creators;
      } else {
        alert(data.message);
        // this.$router.push({ name: "login", params: { role: 'user' } });
      }
    },
    logout() {
      localStorage.removeItem("admin_token");
      this.$router.push("/");
    },
  },
  mounted() {
    this.fetchCreators();
    this.fetchData();
  }
};
</script>

<style scoped>
body {
  margin: 0;
  font-family: "Times New Roman", Times, serif;
  width: 100%;
  height: 100%;
  background: linear-gradient(to right, #F7E5DA, #D6B2B2);
  color: #333;
}

.navbar {
  background-color: #832B00;
  color: #fff;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar h1 {
  margin: 0;
  font-size: 1.5em;
  /* font-style: italic; */
  font-weight: normal;
}

.navbar a {
  text-decoration: none;
  color: #fff;
  font-weight: bold;
  margin: 0 10px;
  /* font-style: italic; */
  transition: color 0.3s ease;
}

.navbar a:hover {
  color: #F7E5DA;
}

.content {
  display: flex;
  justify-content: space-around;
  padding: 20px;
  flex-grow: 1;
}

.uploads-section {
  background-color: rgba(211, 80, 80, 0.1);
  padding: 20px;
  box-shadow: 0 0 0px rgba(224, 10, 10, 0.1);
  border-radius: 8px;
  width: 40%;
  backdrop-filter: blur(3px);
}

.uploads-section h2 {
  font-size: 1.5em;
  margin-bottom: 20px;
  /* font-style: italic; */
  text-align: center;
  color: #000000;
}

.dashboard-sub-container {
  height: 150px;
  border: 1px solid #F7C8C8;
  border-radius: 5px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 15px;
  /* font-style: italic; */
  background-color: #F7E5DA;
}

.dashboard-sub-container div {
  font-size: 28px;
  color: #000000;
  font-weight: bold;
}

.uploads-section table {
  border-collapse: collapse;
  border: 0.5px solid #F7C8C8;
  width: 100%;
  background-color: #F7E5DA;
}

.uploads-section th,
.uploads-section td {
  border: 1px solid #F7C8C8;
  padding: 12px;
  text-align: left;
}

.uploads-section th {
  background-color: #932B2B;
  color: #FBF8F8;
}

.uploads-section a {
  text-decoration: none;
  color: #000000;
}

.uploads-section button {
  cursor: pointer;
  background-color: #b40a0a;
  color: white;
  border: none;
  padding: 8px 12px;
  text-align: center;
  font-size: 14px;
  border-radius: 4px;
  font-weight: bold;
  margin-left: 5px;
  transition: background-color 0.3s ease;
}

.uploads-section button:hover {
  background-color: #B8542E;
}


.Admin {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 15px;
  background-color: rgba(228, 29, 29, 0.2);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.Admin h2 {
  margin-bottom: 10px;
  font-size: 1.5em;
  /* color: #fff; */
}

.Admin a {
  text-decoration: none;
  color: #0d5788;
  font-weight: bold;
}

.container {
  padding: 20px;
  background-color: rgba(237, 17, 17, 0.2);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.app-performance {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.app-subcontainer {
  padding: 15px;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #130e0e;
}
</style>

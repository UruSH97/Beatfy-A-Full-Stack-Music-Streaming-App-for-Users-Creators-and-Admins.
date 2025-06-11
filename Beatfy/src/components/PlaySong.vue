<template>
  <div class="bodyy">
    <div class="navbar">
      <router-link to="/user-dashboard">
        <h1 class="fw-bold"><i class="bi bi-google-play"></i> Beatfy</h1>
      </router-link>
      <div>
        <router-link to="/creator-login">Creator Page</router-link>
        <span @click="logout" style="cursor: pointer;">Logout</span>
      </div>
    </div>

    <div class="content">
      <div class="uploads-section">
        <h2>{{ song.name }}</h2>
        <h5>{{ album.name }} | Rating: {{ song.ratings }}</h5>

        <h5>
          <div class="dropdown">
            <button style="margin-left: 10px;" class="btn dropdown-toggle fw-bold" type="button" data-bs-toggle="dropdown"
              aria-expanded="false">
              Add to Playlist
            </button>
            <ul class="dropdown-menu">
              <template v-for="play in playlists">
                <li class="dropdown-item">
                  <span class="btn" @click="addToPlaylist(play.id, song.id)">{{ play.name }}</span>
                </li>
              </template>
            </ul>
          </div>
        </h5>
        <h2><audio :src=getSong(song.song_url) controls></audio></h2>
        {{ song.lyrics }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      song: {},
      album: {},
      playlists: []
    };
  },
  methods: {
    getSong(song) {
      return `/src/assets/audio/${song}`
    },

    async fetchSong() {
      const url = `http://127.0.0.1:5000/api/song?id=${this.$route.params.id}`;
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          'Authorization': 'Bearer ' + localStorage.getItem(`user_token`),
        },
      });
      const data = await response.json();
      if (response.ok) {
        this.song = data.song;
        this.album = data.song.album;

      } else {
        alert(data.message);
        // this.$router.push({ name: "creator-dashboard" });
      }
    },
    async addToPlaylist(id, song_id) {
      const response = await fetch(`http://127.0.0.1:5000/api/playlist/${id}/${song_id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem(`user_token`),
        },
      });
      const data = await response.json();
      if (response.ok) {
        alert(data.message);
        this.fetchSections();
      } else {
        alert(data.message);
        this.fetchSections();
      }
    },
    async fetchPlaylists() {
      const url = `http://127.0.0.1:5000/api/playlist`;
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          'Authorization': 'Bearer ' + localStorage.getItem(`user_token`),
        },
      });
      const data = await response.json();
      if (response.ok) {
        this.playlists = data.playlists;
      } else {
        alert(data.message);
        // this.$router.push({ name: "login", params: { role: 'user' } });
      }
    },
    logout() {
      localStorage.removeItem("user_token");
      this.$router.push("/");
    },
  },
  mounted() {
    this.fetchSong();
    this.fetchPlaylists();
  }
}
</script>

<style scoped>
.bodyy {
  margin: 0;
  font-family: "Times New Roman", Times, serif;
  width: 100%;
  height: 100%;
  /* background: linear-gradient(to right, #F7E5DA, #832B00); */
  background-color: #F7E5DA;
  color: #832B00;
  padding-bottom: 50px;
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
  width: 70%;
  backdrop-filter: blur(3px);
}

.navbar {
  background-color: #832B00;
  color: #fff;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.uploads-section h2 {
  font-size: 1.5em;
  margin-bottom: 20px;
  /* font-style: italic; */
  text-align: center;
  color: #000000;
}

.uploads-section h5 {
  font-size: 1em;
  margin-bottom: 10px;
  /* font-style: italic; */
  text-align: center;
  color: #000000;
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

.app-name {
  font-size: 1.5em;
  margin-top: 8px;
}


.options {
  display: flex;
}

.options a {
  color: rgb(47, 25, 67);
  margin-right: 20px;
  text-decoration: none;
}

.container {
  width: 1440px;
  height: 350px;
  background-size: cover;
  background-position: center;
  border-radius: 8px;
  box-shadow: 0 0 10px #F7E5DA;
  overflow-x: auto;
  display: flex;
  flex-direction: column;
  margin: 20px auto;
}

h2 {
  margin-bottom: 10px;
  padding: 15px;
  background-color: transparent;
  border-radius: 8px 8px 0 0;
  /* color: white; */
}

.sub-container {
  display: flex;
  gap: 10px;
  overflow-x: auto;
}

.div {
  background-size: cover;
  background-position: center;
  width: 268px;
  min-width: 200px;
  height: 268px;
  max-height: 250px;
  border-radius: 5px;
  display: flex;
  flex-direction: column-reverse;
  align-items: center;
  justify-content: space-between;
  box-shadow: #40e26bb5;
  overflow: hidden;
  position: relative;
  border-radius: 5px;
}

.sub-container div img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.sub-container div .song-details {
  background-color: rgba(0, 0, 0, 0.5);
  padding: 15px;
  width: 100%;
  box-sizing: border-box;
}

button {
  /* background-color: #fff; */
  color: #333;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>
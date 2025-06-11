<template>
  <div class="navbar">
    <router-link to="/creator-dashboard">
      <h1 class="fw-bold"><i class="bi bi-google-play"></i> Beatfy | Creator </h1>
    </router-link>
    <div>
      <router-link to="/add-album">+ Album</router-link>
      <router-link to="/add-song">+ Song</router-link>
      <router-link to="/user-login">UserPage</router-link>
      <span @click="logout" style="cursor: pointer;">Logout</span>
    </div>
  </div>
  <div class="bodyy mt-">
    <div class="content">
      <h1>Edit Song</h1>

      <form @submit.prevent="editSong">
        <!-- {{ albums }} -->
        <label for="album">Select Album</label>
        <select v-model="song.album_id" required>
          <option v-for="album in albums" :key="album.id" :value="album.id">{{ album.name }}</option>
        </select>
        <label for="title">Song Name</label>
        <input type="text" v-model="song.name" id="title" required>

        <label for="artist">Artist</label>
        <input type="text" v-model="song.artist" id="artist" required>

        <label for="lyrics">Lyrics</label>
        <textarea v-model="song.lyrics" id="lyrics" rows="5" required></textarea>

        <button type="submit" class="upload-button">Submit</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      albums: [],
      song: {
        album_id: null,
        name: '',
        artist: '',
        lyrics: '',
      }
    };
  },
  methods: {
    async fetchAlbums() {
      const url = `http://127.0.0.1:5000/api/album`;
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          'Authorization': localStorage.getItem(`creator_token`),
        },
      });
      const data = await response.json();
      if (response.ok) {
        this.albums = data.albums;
      } else {
        alert(data.message);
        this.$router.push({ name: "creator-dashboard" });
      }
    },
    async fetchSong() {
      const url = `http://127.0.0.1:5000/api/song?id=${this.$route.params.id}`;
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          'Authorization': localStorage.getItem(`creator_token`),
        },
      });
      const data = await response.json();
      if (response.ok) {
        this.song.name = data.song.name;
        this.song.artist = data.song.artist;
        this.song.lyrics = data.song.lyrics;
        this.song.album_id = data.song.album.id;
      } else {
        alert(data.message);
        this.$router.push({ name: "creator-dashboard" });
      }
    },
    async editSong() {
      const formData = new FormData();
      formData.append('album_id', this.song.album_id);
      formData.append('name', this.song.name);
      formData.append('artist', this.song.artist);
      formData.append('lyrics', this.song.lyrics);

      const response = await fetch(`http://127.0.0.1:5000/api/song/${this.$route.params.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem(`creator_token`),
        },
        body: formData
      });
      const data = await response.json();
      if (response.ok) {
        alert(data.message);
      } else {
        alert(data.message);
      }
      this.$router.push({ name: "creator-dashboard" });
    }
  },
  mounted() {
    this.fetchAlbums();
    this.fetchSong();
  }
};
</script>

<style scoped>
.bodyy {
  margin: 0;
  font-family: "Times New Roman", Times, serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  background: #F7E5DA;
  color: #832B00;
}

.navbar {
  background-color: #832B00;
  color: #F7E5DA;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.navbar h1 {
  margin: 0;
  font-size: 1.5em;
}

.navbar a {
  text-decoration: none;
  color: #F7E5DA;
  font-weight: bold;
  margin: 0 15px;
}

.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 20px 0;
  background-color: #F7E5DA;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
  width: 80%;
  max-width: 800px;
}

h1 {
  font-size: 2em;
  margin-bottom: 15px;
}

form {
  width: 100%;
  max-width: 600px;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #F7E5DA;
}

label {
  font-weight: bold;
  margin-bottom: 10px;
}

input,
textarea,
select {
  width: calc(100% - 20px);
  padding: 8px;
  margin-bottom: 20px;
  border: 1px solid #832B00;
  border-radius: 8px;
  outline: none;
}

.upload-button {
  background-color: #832B00;
  color: #F7E5DA;
  border: none;
  padding: 10px;
  text-align: center;
  text-decoration: none;
  font-size: 18px;
  cursor: pointer;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.upload-button:hover {
  background-color: #6B2300;
}
</style>
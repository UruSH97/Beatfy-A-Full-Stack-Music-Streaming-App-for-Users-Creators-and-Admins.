<template>
  <div>
    <div class="navbar">
      <router-link to="/creator-dashboard">
        <h1 class="fw-bold"><i class="bi bi-google-play"></i> Beatfy | Creator </h1>
      </router-link>
      <div>
        <router-link to="/add-album">+ Album</router-link>
        <router-link to="/add-song">+ Song</router-link>
        <router-link to="/user-login">User Page</router-link>
        <span @click="logout" style="cursor: pointer;">Logout</span>
      </div>
    </div>

    <div class="content">
      <div class="uploads-section">
        <h2>Your Albums</h2>
        <table>
          <thead>
            <tr>
              <th>Album Name</th>
              <th>Artist</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="album in albums" :key="album.id">
              <td @click="viewAlbum(album.id)" style="cursor: pointer;">{{ album.name }}</td>
              <td>{{ album.artist }}</td>
              <td style="width: 150px;">
                <button @click="editAlbum(album.id)">Edit</button>
                <button @click="deleteAlbum(album.id)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="uploads-section">
        <h2>Your Songs</h2>
        <table>
          <thead>
            <tr>
              <th>Song</th>
              <th>Album</th>
              <th>Artist</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="song in songs" :key="song.id">
              <td @click="playTrack(song.id)" style="cursor: pointer;">{{ song.name }}</td>
              <td>{{ song.album.name }}</td>
              <td>{{ song.artist }}</td>
              <td style="width: 150px;">
                <button @click="editSong(song.id)">Edit</button>
                <button @click="deleteSong(song.id)">Delete</button>
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
      songs: [],
      albums: [],
    };
  },
  methods: {
    viewAlbum(id) {
      this.$router.push({ name: "album-page", params: { id: id } });
    },
    playTrack(id) {
      this.$router.push({ name: "song-page", params: { id: id } });
    },
    editAlbum(id) {
      this.$router.push({ name: "edit-album", params: { id: id } });
    },
    editSong(id) {
      this.$router.push({ name: "edit-song", params: { id: id } });
    },
    async deleteSong(Id) {
      const confirmation = confirm("Are you sure you want to delete this song?");
      if (confirmation) {
        const response = await fetch(`http://127.0.0.1:5000/api/song/${Id}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem(`creator_token`)
          },
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.fetchSongs();
        } else {
          alert(data.message);
          this.fetchSongs();
        }
      }
    },
    async deleteAlbum(Id) {
      const confirmation = confirm("Are you sure you want to delete this album?");
      if (confirmation) {
        const response = await fetch(`http://127.0.0.1:5000/api/album/${Id}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem(`creator_token`)
          },
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.fetchAlbums();
          this.fetchSongs();
        } else {
          alert(data.message);
          this.fetchAlbums();
          this.fetchSongs();
        }
      }
    },

    async fetchAlbums() {
      const url = `http://127.0.0.1:5000/api/album`;
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          'Authorization': 'Bearer ' + localStorage.getItem(`creator_token`),
        },
      });
      const data = await response.json();
      if (response.ok) {
        this.albums = data.albums;
      } else {
        alert(data.message);
        // this.$router.push({ name: "login", params: { role: 'user' } });
      }
    },
    async fetchSongs() {
      const url = `http://127.0.0.1:5000/api/song`;
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          'Authorization': 'Bearer ' + localStorage.getItem(`creator_token`),
        },
      });
      const data = await response.json();
      if (response.ok) {
        this.songs = data.songs;
      } else {
        alert(data.message);
        // this.$router.push({ name: "login", params: { role: 'user' } });
      }
    },
    logout() {
      localStorage.removeItem("creator_token");
      this.$router.push("/");
    },
  },
  mounted() {
    this.fetchAlbums();
    this.fetchSongs();
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
  width: 50%;
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
</style>

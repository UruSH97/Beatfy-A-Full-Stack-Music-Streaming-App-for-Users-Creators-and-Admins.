<template>
  <div class="bodyy">
    <div class="navbar">
      <router-link to="/user-dashboard">
        <h1 class="fw-bold"><i class="bi bi-google-play"></i> Beatfy</h1>
      </router-link>

      <input type="text" class="form-control" id="search_input" name="searchQuery"
        placeholder="Search for songs, artists ........."
        style="position: relative; width:530px; height:30px; border:1px solid black; border-radius:30px;"
        @keyup.enter="search" v-model="searchQuery">

      <div>
        <span @click="createPlaylist">+ Playlist</span>
        <router-link to="/creator-login">Creator Page</router-link>
        <span @click="logout" style="cursor: pointer;">Logout</span>
      </div>
    </div>


    <!-- Song container -->
    <div class="container">
      <h2>Top Songs</h2>
      <div class="sub-container">
        <!-- Iterate through trending searches -->
        <!-- Render each track -->
        <div class="track" v-for="track in songs" :key="track.id"
          :style="'background-image: url(' + getUrl('bg.jpeg') + ')'">
          <div class="song-details fs-5">
            <span @click="playTrack(track.id)" style="cursor: pointer;">{{ track.name }}</span>
            <p @click="rateSong(track.id)" style="cursor: pointer;"> <i class="bi bi-star-fill text-warning"></i> {{
          track.ratings }}</p>
            <!-- <button >Play</button> -->
          </div>
        </div>
      </div>
    </div>

    <!-- Album container -->
    <div class="container">
      <h2>Albums</h2>
      <!-- {{ albums }} -->
      <div class="sub-container">
        <!-- Render each album -->
        <div class="genre" v-for="album in  albums " :key="album.id"
          :style="'background-image: url(' + getUrl('ab.jpg') + ')'">
          <div class="song-details" style="padding-bottom: 35px; cursor: pointer;" @click="viewAlbum(album.id)">
            <span>{{ album.name }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Playlist container -->
    <div class="container">
      <h2>Your Playlists</h2>
      <div class="sub-container">
        <!-- Iterate through user playlists -->
        <!-- Render each playlist -->
        <div class="playlist" v-for="playlist in playlists" :key="playlist.id" :data-playlist-id="playlist.id"
          :style="'background-image: url(' + getUrl('pl.jpg') + ')'">
          <div class="song-details" style="padding-bottom: 0px;">
            <span class="fs-5" style="cursor: pointer;" @click="viewPlaylist(playlist.id)">{{ playlist.name }}</span>
            <button @click="deletePlaylist(playlist.id)" style="margin-top: 25px; border-radius: 20px;"><i
                class="bi bi-trash3"></i></button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
      songs: [],
      playlists: [],
      albums: []
    };
  },
  methods: {
    search() {
        this.$router.push({ name: "search-song", query: { q: this.searchQuery } });
    },
    viewPlaylist(id) {
      this.$router.push({ name: "view-playlist", params: { id: id } });
    },
    viewAlbum(id) {
      this.$router.push({ name: "view-album", params: { id: id } });
    },
    playTrack(id) {
      this.$router.push({ name: "play-song", params: { id: id } });
    },
    getUrl(file) {
      return `/src/assets/${file}`
    },
    async fetchAlbums() {
      const url = `http://127.0.0.1:5000/api/album`;
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          'Authorization': 'Bearer ' + localStorage.getItem(`user_token`),
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
          'Authorization': 'Bearer ' + localStorage.getItem(`user_token`),
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
    async createPlaylist() {
      let name = prompt("Enter the playlist name:");

      if (!name || name.length < 0) {
        alert("Invalid playlist name!");
        return;
      }

      const response = await fetch(`http://127.0.0.1:5000/api/playlist`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + localStorage.getItem(`user_token`)
          },
          body: JSON.stringify({ name: name }),
        }
      );

      const data = await response.json();
      if (response.ok) {
        alert(data.message);
        this.fetchPlaylists();
      } else {
        alert(data.message);
        this.fetchPlaylists();
      }
    },
    async rateSong(id) {
      let rating = prompt("Enter a rating between 1-5: ");
      rating = parseFloat(rating)

      if (!rating || rating < 0 || rating > 5) {
        alert("Invalid rating!");
        return;
      }

      const response = await fetch(`http://127.0.0.1:5000/api/song/${id}`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + localStorage.getItem(`user_token`)
          },
          body: JSON.stringify({ rating: rating }),
        }
      );

      const data = await response.json();
      if (response.ok) {
        alert(data.message);
        this.fetchSongs();
      } else {
        alert(data.message);
        this.fetchSongs();
      }
    },
    async deletePlaylist(Id) {
      const confirmation = confirm("Are you sure you want to delete this playlist?");
      if (confirmation) {
        const response = await fetch(`http://127.0.0.1:5000/api/playlist/${Id}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem(`user_token`)
          },
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.fetchPlaylists();
        } else {
          alert(data.message);
          this.fetchPlaylists();
        }
      }
    },
    logout() {
      localStorage.removeItem("user_token");
      this.$router.push("/");
    },
  },
  mounted() {
    this.fetchAlbums();
    this.fetchSongs();
    this.fetchPlaylists();
  }
};
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

.search-bar {
  flex-grow: 2;
  margin: 0 20px;
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
  height: 340px;
  background-size: cover;
  background-color: #832B00;
  background-position: center;
  border-radius: 8px;
  box-shadow: 0 0 10px #F7E5DA;
  overflow-x: auto;
  display: flex;
  flex-direction: column;
  margin: 20px auto;
  /* padding: 20px; */
}

h2 {
  /* margin-bottom: 10px; */
  padding: 10px;
  background-color: transparent;
  border-radius: 8px 8px 0 0;
  color: white;
}

.sub-container {
  display: flex;
  gap: 10px;
  overflow-x: auto;

}

.sub-container div {
  color: white;
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

import { createRouter, createWebHistory } from 'vue-router'

import AdminDashboard from '../components/AdminDashboard.vue'
import CreatorDashboard from '../components/CreatorDashboard.vue'
import UserDashboard from '../components/UserDashboard.vue'

import Home from '../views/Home.vue'
import Register from '../components/Register.vue'
import AdminLogin from '../components/AdminLogin.vue'
import UserLogin from '../components/UserLogin.vue'
import CreatorLogin from '../components/CreatorLogin.vue'

import AlbumForm from '../components/AlbumForm.vue'
import EditAlbum from '../components/EditAlbum.vue'
import SongForm from '../components/SongForm.vue'
import EditSong from '../components/EditSong.vue'

import PlaySong from '../components/PlaySong.vue'
import PlaylistView from '../components/PlaylistView.vue'
import AlbumView from '../components/AlbumView.vue'
import SearchSong from '../components/SearchSong.vue'

import AlbumPage from '../components/AlbumPage.vue'
import SongPage from '../components/SongPage.vue'
import AdminPage from '../components/AdminPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: "/admin-login",
      name: "admin-login",
      component: AdminLogin,
    },
    {
      path: "/user-login",
      name: "user-login",
      component: UserLogin,
    },
    {
      path: "/creator-login",
      name: "creator-login",
      component: CreatorLogin,
    },
    {
      path: "/user-register",
      name: "register",
      component: Register,
    },
    {
      path: "/admin-dashboard",
      name: "admin-dashboard",
      component: AdminDashboard,
    },
    {
      path: "/manage",
      name: "manage",
      component: AdminPage,
    },
    {
      path: "/creator-dashboard",
      name: "creator-dashboard",
      component: CreatorDashboard,
    },
    {
      path: "/user-dashboard",
      name: "user-dashboard",
      component: UserDashboard,
    },
    {
      path: "/search",
      name: "search-song",
      component: SearchSong,
    },
    {
      path: "/edit-album/:id",
      name: "edit-album",
      component: EditAlbum,
    },
    {
      path: "/add-song",
      name: "add-song",
      component: SongForm,
    },
    {
      path: "/add-album",
      name: "add-album",
      component: AlbumForm,
    },
    {
      path: "/edit-song/:id",
      name: "edit-song",
      component: EditSong,
    },
    {
      path: "/play-song/:id",
      name: "play-song",
      component: PlaySong,
    },
    {
      path: "/view-playlist/:id",
      name: "view-playlist",
      component: PlaylistView,
    },
    {
      path: "/view-album/:id",
      name: "view-album",
      component: AlbumView,
    },
    {
      path: "/album-page/:id",
      name: "album-page",
      component: AlbumPage,
    },
    {
      path: "/song-page/:id",
      name: "song-page",
      component: SongPage,
    },
  ]
})

export default router

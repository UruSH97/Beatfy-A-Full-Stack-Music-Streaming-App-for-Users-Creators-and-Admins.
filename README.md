# 🎵 Beatfy – A Full-Stack Music Streaming Platform

Beatfy is a feature-rich, scalable music streaming application that supports multiple user roles — **Users**, **Creators**, and **Admins** — each with customized access and controls. Built with **Vue 3**, **Vite**, and a structured relational database, Beatfy brings together music playback, lyrics integration, playlist management, and admin moderation in one seamless platform.

---

## 🚀 Features

### 👤 User Functions
- Sign up and login with token-based authentication
- Stream songs and view lyrics in real-time
- Rate songs and view average ratings
- Create, manage, and delete playlists
- Search songs and albums by name, artist, or rating
- Receive email reminders if inactive for extended periods

### ✍️ Creator Functions
- All User functionalities, plus:
- Upload and manage songs, albums, and lyrics
- Export activity reports as CSV (songs uploaded, ratings, etc.)
- View monthly reports of their contributions

### 🛡️ Admin Functions
- View platform-wide statistics (total songs, albums, creators)
- Monitor and block inappropriate songs, albums, or creators
- View top-rated songs and usage metrics
- Manage user permissions and handle reported content

---

## 🧱 Database Schema

### Tables & Key Fields
- **Admin**: `admin_id`, `adminname`, `email`
- **User**: `user_id`, `username`, `last_login`, `is_creator`
- **Album**: `id`, `name`, `artist`, `user_id`
- **Song**: `id`, `name`, `artist`, `lyrics`, `song_url`, `album_id`, `user_id`, `ratings`
- **Playlist**: `id`, `name`, `user_id`
- **Playlist_Songs**: Many-to-Many relationship between songs and playlists

---

## 🔍 Additional Functionalities

- **Lyrics display** embedded in the streaming screen
- **Creator dashboard** to manage contributions
- **Monthly creator email reports**
- **Admin analytics** and song ranking features
- **Add multiple songs/albums at once**
- **Responsive and interactive UI**

---

## 🛠️ Tech Stack

- **Frontend**: Vue 3, Vite, JavaScript
- **Backend/DB**: (Assumed) SQL-based relational DB
- **Authentication**: Token-based login system
- **Data Export**: CSV generation for creator analytics
- **Dev Tools**: VS Code, Volar, Node.js

---

## 🧪 Setup Instructions

### Clone and Install

```bash
git clone https://github.com/yourusername/beatfy.git
cd beatfy
npm install


### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

## 🎬 Demo

You can watch the full demo of Beatfy in action here:  
👉 [Watch Demo Video](https://drive.google.com/file/d/1joIa3zq7MpkHTIsnSxMXrS4Y7oX7RwD2/view?usp=drive_link)






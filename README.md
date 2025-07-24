# Beatfy – A Full-Stack Music Streaming Platform

## About

Beatfy is a full-stack music streaming application designed to serve three distinct user roles — Users, Creators, and Admins — each with tailored capabilities. Built using Vue 3 and a structured relational database, Beatfy provides a responsive music experience that includes real-time playback, playlist creation, lyrics display, and powerful admin controls. 

The platform supports music streaming, playlist management, song ratings, lyrics integration, and role-based access — all in one cohesive interface. It also includes moderation features for administrators and content publishing tools for creators.

---

## Features

### User Functionality

- Sign up and login using a secure token-based system
- Stream music and view lyrics in real time
- Rate songs and view average ratings from others
- Create and manage personal playlists
- Search songs and albums by name, artist, or rating
- Receive automated email reminders when inactive

### Creator Functionality

- All standard user functions, plus:
- Upload songs, albums, and lyrics
- Manage uploaded content from a dedicated dashboard
- Export activity and performance reports as CSV
- View monthly summaries of content performance

### Admin Functionality

- Access platform-wide statistics (songs, albums, creators)
- View, block, or remove flagged songs, albums, or creators
- Review top-rated content and usage metrics
- Manage permissions and moderate user-reported items

---

## Database Schema

Key tables and fields include:

- `Admin`: admin_id, adminname, email  
- `User`: user_id, username, last_login, is_creator  
- `Album`: id, name, artist, user_id  
- `Song`: id, name, artist, lyrics, song_url, album_id, user_id, ratings  
- `Playlist`: id, name, user_id  
- `Playlist_Songs`: linking table for songs and playlists (many-to-many)

---

## Additional Features

- Embedded lyrics viewer in the streaming interface
- Creator dashboard for uploads and statistics
- Automated monthly reports to creators via email
- Administrative analytics, ranking, and moderation controls
- Bulk upload functionality for songs and albums
- Fully responsive and interactive frontend design

---

## Tech Stack

- **Frontend**: Vue 3, Vite, JavaScript
- **Backend**: SQL-based relational database (assumed)
- **Authentication**: Token-based login and session management
- **Data Export**: CSV reports for creator dashboards
- **Dev Environment**: VS Code, Node.js, Volar

---

## Setup Instructions

1. Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/beatfy.git
cd beatfy
npm install
```

2. To run in development mode:

```bash
npm run dev
```

3. To build for production:

```bash
npm run build
```

---

## Demo

A full walkthrough of the Beatfy platform is available in the demo video.  
Link: [Watch Demo Video](#)

---

## Contributions

If you’d like to enhance Beatfy or suggest improvements, feel free to fork the repo and submit a pull request.
README ... tfy.md
Displaying README_Beatfy.md.

# 📜 The Library of Ohara — Cinematic Archive & Watchlist

> *"Books and cinema are the vessel of collective human memory. Even if an island is erased, the knowledge inscribed in our hearts will forever endure."*

The **Library of Ohara** is a React-powered cinematic archive web application where scholars and explorers can discover cinematic history, investigate detailed movie archives, maintain a persistent personal watchlist, and curate historical logs.

---

## 🌟 Key Features

1. **🏛️ Archive Codex & Discover (Home)**:
   - Spotlight Hero Carousel showcasing trending cinematic artifacts with backdrops, ratings, and instant actions.
   - Quick Genre exploration pills.
   - Categorized tabs for *Popular Relics*, *Trending Records*, *Top Rated Classics*, and *Upcoming Chronicles*.
   - Ranked Sidebar featuring *Scholars' Masterpieces* and *Active Inquiries*.

2. **🔍 Search Grimoire (Search & Filter)**:
   - Dynamic real-time query search across titles, directors, and overviews.
   - Filter by full genre classifications (Action, Sci-Fi, Animation, Drama, Fantasy, Crime, etc.).
   - Sort by *Highest Rated*, *Newest Release*, *Earliest Classic*, and *Alphabetical*.

3. **📜 Detailed Artifact Inspection (MovieDetails)**:
   - High-resolution cinematic backdrop banner with atmospheric gradient overlay.
   - Complete metadata: Release year, runtime, director, score, and genre badges.
   - Distinguished cast list with profile portraits and character names.
   - **Preview Vision**: Embedded YouTube movie trailer / teaser modal.
   - **Scholar's Log**: Custom curation box allowing users to set Watch Status (*Plan to Watch*, *Studying*, *Completed*, *Favorite*), assign a personal Scholar Star Rating (1-10), and write personal study notes.
   - Related Ancient Chronicles shelf.

4. **🔖 Scholar's Personal Codex (Persistent Watchlist)**:
   - Persistent storage backed by `localStorage`.
   - Statistics dashboard calculating Total Archived Scrolls, Study Duration in Hours, Treasured Gems (Favorites), and Fully Mastered films.
   - Filter collection by status (*All*, *Plan to Watch*, *Studying*, *Completed*, *Favorites*).
   - **Export Codex**: Download your entire archive as a portable JSON backup.
   - **Import Codex**: Restore and synchronize your archive from any JSON scroll backup.

5. **🌐 TMDB & Autonomous Mock Model Integration**:
   - Supports live **The Movie Database (TMDB) API** when configured with `VITE_TMDB_API_KEY`.
   - Built-in comprehensive high-fidelity **Mock Database** (Sci-Fi, Classics, Animation, Action, Anime) ensuring 100% offline & demo reliability with zero setup required.

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment (Optional)
In [.env](.env):
```env
VITE_TMDB_API_KEY=your_api_key_here
VITE_USE_MOCK=false
```
*Note: If `VITE_USE_MOCK=true` or no API key is provided, the application runs seamlessly using the built-in offline archive.*

### 3. Run Development Server
```bash
npm run dev
```

### 4. Build for Production
```bash
npm run build
```

---

## 🛠️ Architecture & Tech Stack

- **Framework**: React 18 + Vite
- **Routing**: React Router DOM v6
- **Styling**: Pure Modern CSS with Ancient Scholar Glassmorphism, CSS Custom Properties, and responsive grid layouts
- **Icons**: Lucide React
- **Typography**: Google Fonts (*Cinzel* for ancient headers & *Outfit* for modern readability)
- **Data Layer**: TMDB API + Local Autonomous Dataset + LocalStorage state synchronizer

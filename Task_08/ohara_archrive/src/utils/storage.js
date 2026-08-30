/**
 * Library of Ohara - Persistent Scholar Storage Utilities
 * Manages localStorage for curated movie records, custom notes, statuses, and export/import.
 */

const WATCHLIST_KEY = 'ohara_scholars_archive_v2';

export function getWatchlist() {
  try {
    const data = localStorage.getItem(WATCHLIST_KEY);
    if (!data) return [];
    const parsed = JSON.parse(data);
    return Array.isArray(parsed) ? parsed : [];
  } catch (error) {
    console.error('Failed to parse Ohara archive storage:', error);
    return [];
  }
}

export function saveWatchlist(movies) {
  try {
    localStorage.setItem(WATCHLIST_KEY, JSON.stringify(movies));
  } catch (error) {
    console.error('Failed to save to Ohara archive storage:', error);
  }
}

export function isInWatchlist(id) {
  const list = getWatchlist();
  return list.some(item => Number(item.id) === Number(id));
}

export function getWatchlistItem(id) {
  const list = getWatchlist();
  return list.find(item => Number(item.id) === Number(id)) || null;
}

export function addToWatchlist(movie, status = 'plan_to_watch', notes = '', scholarRating = null) {
  const list = getWatchlist();
  const existingIndex = list.findIndex(m => Number(m.id) === Number(movie.id));
  
  const entry = {
    id: movie.id,
    title: movie.title,
    poster_path: movie.poster_path,
    backdrop_path: movie.backdrop_path,
    vote_average: movie.vote_average,
    release_date: movie.release_date,
    genres: movie.genres || [],
    runtime: movie.runtime || 120,
    overview: movie.overview,
    status: status, // 'plan_to_watch' | 'watching' | 'completed' | 'favorite'
    notes: notes || '',
    scholarRating: scholarRating,
    archivedAt: new Date().toISOString()
  };

  if (existingIndex >= 0) {
    list[existingIndex] = { ...list[existingIndex], ...entry };
  } else {
    list.unshift(entry);
  }

  saveWatchlist(list);
  return entry;
}

export function updateWatchlistEntry(id, updates) {
  const list = getWatchlist();
  const index = list.findIndex(m => Number(m.id) === Number(id));
  if (index >= 0) {
    list[index] = { ...list[index], ...updates, updatedAt: new Date().toISOString() };
    saveWatchlist(list);
    return list[index];
  }
  return null;
}

export function removeFromWatchlist(id) {
  const list = getWatchlist();
  const updated = list.filter(m => Number(m.id) !== Number(id));
  saveWatchlist(updated);
  return updated;
}

export function exportArchiveAsJSON() {
  const list = getWatchlist();
  const blob = new Blob([JSON.stringify(list, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `ohara_archive_scroll_${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

export function importArchiveFromJSON(jsonString) {
  try {
    const data = JSON.parse(jsonString);
    if (Array.isArray(data)) {
      saveWatchlist(data);
      return data;
    }
  } catch (err) {
    throw new Error('Invalid Ohara archive scroll JSON format.');
  }
  return null;
}
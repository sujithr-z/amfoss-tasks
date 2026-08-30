import { useState, useEffect, useCallback } from 'react';
import {
  getWatchlist,
  saveWatchlist,
  isInWatchlist as checkInWatchlist,
  getWatchlistItem,
  addToWatchlist as addStorage,
  removeFromWatchlist as removeStorage,
  updateWatchlistEntry as updateStorage,
  exportArchiveAsJSON,
  importArchiveFromJSON
} from '../utils/storage';

export function useWatchlist() {
  const [watchlist, setWatchlist] = useState(() => getWatchlist());

  // Listen to custom storage events to keep tabs or components synchronized
  useEffect(() => {
    const handleStorageChange = () => {
      setWatchlist(getWatchlist());
    };

    window.addEventListener('storage', handleStorageChange);
    window.addEventListener('ohara_watchlist_updated', handleStorageChange);
    return () => {
      window.removeEventListener('storage', handleStorageChange);
      window.removeEventListener('ohara_watchlist_updated', handleStorageChange);
    };
  }, []);

  const notifyChange = () => {
    window.dispatchEvent(new Event('ohara_watchlist_updated'));
    setWatchlist(getWatchlist());
  };

  const addToWatchlist = useCallback((movie, status = 'plan_to_watch', notes = '', rating = null) => {
    addStorage(movie, status, notes, rating);
    notifyChange();
  }, []);

  const removeFromWatchlist = useCallback((id) => {
    removeStorage(id);
    notifyChange();
  }, []);

  const updateEntry = useCallback((id, updates) => {
    updateStorage(id, updates);
    notifyChange();
  }, []);

  const toggleWatchlist = useCallback((movie) => {
    if (checkInWatchlist(movie.id)) {
      removeStorage(movie.id);
    } else {
      addStorage(movie);
    }
    notifyChange();
  }, []);

  const isInWatchlist = useCallback((id) => {
    return checkInWatchlist(id);
  }, [watchlist]);

  const getEntry = useCallback((id) => {
    return getWatchlistItem(id);
  }, [watchlist]);

  const exportArchive = useCallback(() => {
    exportArchiveAsJSON();
  }, []);

  const importArchive = useCallback((jsonStr) => {
    const res = importArchiveFromJSON(jsonStr);
    notifyChange();
    return res;
  }, []);

  // Stats calculation
  const stats = {
    total: watchlist.length,
    favorites: watchlist.filter(m => m.status === 'favorite').length,
    completed: watchlist.filter(m => m.status === 'completed').length,
    planToWatch: watchlist.filter(m => m.status === 'plan_to_watch').length,
    totalMinutes: watchlist.reduce((acc, m) => acc + (Number(m.runtime) || 120), 0)
  };

  return {
    watchlist,
    stats,
    addToWatchlist,
    removeFromWatchlist,
    updateEntry,
    toggleWatchlist,
    isInWatchlist,
    getEntry,
    exportArchive,
    importArchive
  };
}
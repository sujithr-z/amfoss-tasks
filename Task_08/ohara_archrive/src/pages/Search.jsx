import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { searchMovies, getGenres } from '../services/tmdb';
import MovieGrid from '../components/MovieGrid';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';
import { Search as SearchIcon, Filter, X, SlidersHorizontal, Sparkles } from 'lucide-react';
import './Search.css';

export default function Search() {
  const [searchParams, setSearchParams] = useSearchParams();
  const queryParam = searchParams.get('q') || '';
  const genreParam = searchParams.get('genre') || '';

  const [inputQuery, setInputQuery] = useState(queryParam);
  const [selectedGenre, setSelectedGenre] = useState(genreParam);
  const [sortBy, setSortBy] = useState('rating_desc');
  const [genres, setGenres] = useState([]);
  
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load genres
  useEffect(() => {
    getGenres().then((data) => setGenres(data || []));
  }, []);

  // Sync params when URL changes
  useEffect(() => {
    setInputQuery(queryParam);
    setSelectedGenre(genreParam);
  }, [queryParam, genreParam]);

  // Execute Search
  useEffect(() => {
    const fetchSearchResults = async () => {
      setLoading(true);
      setError(null);
      try {
        const results = await searchMovies(queryParam, genreParam);
        
        // Sorting logic
        let sorted = [...(results || [])];
        if (sortBy === 'rating_desc') {
          sorted.sort((a, b) => (b.vote_average || 0) - (a.vote_average || 0));
        } else if (sortBy === 'release_desc') {
          sorted.sort((a, b) => new Date(b.release_date || 0) - new Date(a.release_date || 0));
        } else if (sortBy === 'release_asc') {
          sorted.sort((a, b) => new Date(a.release_date || 0) - new Date(b.release_date || 0));
        } else if (sortBy === 'title_asc') {
          sorted.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
        }

        setMovies(sorted);
      } catch (err) {
        console.error("Search error:", err);
        setError("An ancient distortion prevented the search results from materializing.");
      } finally {
        setLoading(false);
      }
    };

    fetchSearchResults();
  }, [queryParam, genreParam, sortBy]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    updateQueryParams(inputQuery, selectedGenre);
  };

  const handleGenreClick = (genreId) => {
    const nextGenre = selectedGenre === String(genreId) ? '' : String(genreId);
    setSelectedGenre(nextGenre);
    updateQueryParams(inputQuery, nextGenre);
  };

  const updateQueryParams = (q, g) => {
    const params = {};
    if (q.trim()) params.q = q.trim();
    if (g) params.genre = g;
    setSearchParams(params);
  };

  const clearAllFilters = () => {
    setInputQuery('');
    setSelectedGenre('');
    setSearchParams({});
  };

  const selectedGenreObj = genres.find(g => String(g.id) === String(selectedGenre));

  return (
    <div className="ohara-search-page">
      {/* SEARCH HEADER */}
      <div className="search-header-container">
        <div className="search-title-wrap">
          <div className="badge-gold">
            <Sparkles size={13} />
            SEARCH THE VAULT
          </div>
          <h1>Search the Ohara Cinematic Codex</h1>
          <p>Query over thousands of ancient and modern film artifacts stored across time.</p>
        </div>

        {/* Big Search Bar */}
        <form onSubmit={handleSearchSubmit} className="search-hero-form">
          <div className="search-input-box">
            <SearchIcon size={20} className="search-lens" />
            <input
              type="text"
              placeholder="Search by title, director, keywords..."
              value={inputQuery}
              onChange={(e) => setInputQuery(e.target.value)}
            />
            {inputQuery && (
              <button 
                type="button" 
                className="input-clear"
                onClick={() => setInputQuery('')}
              >
                <X size={16} />
              </button>
            )}
          </div>
          <button type="submit" className="btn-ohara btn-ohara-primary search-action-btn">
            Search
          </button>
        </form>

        {/* GENRE FILTERS ROW */}
        <div className="genre-filter-bar">
          <div className="filter-label">
            <Filter size={14} />
            <span>Filter by Genre:</span>
          </div>
          <div className="genre-pill-list">
            <button
              type="button"
              className={`genre-filter-pill ${!selectedGenre ? 'active' : ''}`}
              onClick={() => handleGenreClick('')}
            >
              All Genres
            </button>
            {genres.map((g) => (
              <button
                key={g.id}
                type="button"
                className={`genre-filter-pill ${selectedGenre === String(g.id) ? 'active' : ''}`}
                onClick={() => handleGenreClick(g.id)}
              >
                {g.name}
              </button>
            ))}
          </div>
        </div>

        {/* SORT & ACTIVE FILTERS BAR */}
        <div className="search-controls-bar">
          <div className="results-summary">
            {!loading && (
              <span>
                Found <strong>{movies.length}</strong> {movies.length === 1 ? 'scroll' : 'scrolls'}
                {queryParam && <> for <em>"{queryParam}"</em></>}
                {selectedGenreObj && <> in <strong>{selectedGenreObj.name}</strong></>}
              </span>
            )}
          </div>

          <div className="sort-controls">
            <SlidersHorizontal size={14} />
            <label htmlFor="sortSelect">Sort Order:</label>
            <select
              id="sortSelect"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="sort-dropdown"
            >
              <option value="rating_desc">Highest Rated</option>
              <option value="release_desc">Newest Release</option>
              <option value="release_asc">Earliest Classic</option>
              <option value="title_asc">Title (A-Z)</option>
            </select>

            {(queryParam || selectedGenre) && (
              <button onClick={clearAllFilters} className="clear-filters-btn">
                <X size={14} />
                <span>Reset</span>
              </button>
            )}
          </div>
        </div>
      </div>

      {/* RESULTS DISPLAY */}
      <div className="search-results-container">
        {loading ? (
          <Loading message="Deciphering matching scrolls..." />
        ) : error ? (
          <ErrorMessage message={error} onRetry={() => window.location.reload()} />
        ) : (
          <MovieGrid 
            movies={movies} 
            emptyMessage={queryParam ? `No records found matching "${queryParam}". Try seeking other historical titles.` : "Select a genre or enter a keyword to begin your inquiry."}
            emptyCtaLink="/"
            emptyCtaText="Return to Main Archive"
          />
        )}
      </div>
    </div>
  );
}
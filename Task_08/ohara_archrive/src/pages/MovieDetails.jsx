import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getMovieDetails, getImageUrl } from '../services/tmdb';
import { useWatchlist } from '../hooks/useWatchlist';
import MovieCard from '../components/MovieCard';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';
import { 
  Star, 
  Clock, 
  Calendar, 
  Bookmark, 
  Check, 
  ArrowLeft, 
  Play, 
  X, 
  User, 
  Scroll, 
  Heart, 
  Eye, 
  FileText,
  Sparkles
} from 'lucide-react';
import './MovieDetails.css';

export default function MovieDetails() {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showTrailerModal, setShowTrailerModal] = useState(false);

  // Watchlist & Custom Scholar Notes
  const { isInWatchlist, getEntry, addToWatchlist, removeFromWatchlist } = useWatchlist();
  
  const savedEntry = movie ? getEntry(movie.id) : null;
  const inWatchlist = movie ? isInWatchlist(movie.id) : false;

  const [status, setStatus] = useState('plan_to_watch');
  const [notes, setNotes] = useState('');
  const [scholarRating, setScholarRating] = useState(0);
  const [notesSavedToast, setNotesSavedToast] = useState(false);

  useEffect(() => {
    const fetchDetails = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await getMovieDetails(id);
        setMovie(data);
      } catch (err) {
        console.error("Failed to load movie details:", err);
        setError("This ancient scroll could not be deciphered or does not exist.");
      } finally {
        setLoading(false);
      }
    };

    fetchDetails();
    window.scrollTo(0, 0);
  }, [id]);

  // Sync entry state when savedEntry changes
  useEffect(() => {
    if (savedEntry) {
      setStatus(savedEntry.status || 'plan_to_watch');
      setNotes(savedEntry.notes || '');
      setScholarRating(savedEntry.scholarRating || 0);
    } else {
      setStatus('plan_to_watch');
      setNotes('');
      setScholarRating(0);
    }
  }, [savedEntry, id]);

  const handleSaveWatchlist = (e) => {
    e.preventDefault();
    if (!movie) return;
    addToWatchlist(movie, status, notes, scholarRating);
    setNotesSavedToast(true);
    setTimeout(() => setNotesSavedToast(false), 3000);
  };

  const handleRemove = () => {
    if (!movie) return;
    removeFromWatchlist(movie.id);
  };

  if (loading) return <Loading message="Retrieving sacred records from the archive vault..." />;
  if (error || !movie) return <ErrorMessage message={error || "Record not found in the Library."} />;

  const releaseYear = movie.release_date ? movie.release_date.split('-')[0] : 'Ancient Era';
  const rating = movie.vote_average ? Number(movie.vote_average).toFixed(1) : 'N/A';
  const backdropUrl = getImageUrl(movie.backdrop_path || movie.poster_path, 'original');
  const posterUrl = getImageUrl(movie.poster_path);

  return (
    <div className="ohara-movie-details-page">
      {/* IMMERSIVE BACKDROP */}
      <div className="details-hero-backdrop" style={{ backgroundImage: `url(${backdropUrl})` }}>
        <div className="details-hero-overlay"></div>
      </div>

      <div className="details-main-container">
        {/* Back Link */}
        <Link to="/" className="details-back-link">
          <ArrowLeft size={16} />
          <span>Back to Library Archive</span>
        </Link>

        <div className="details-layout-grid">
          {/* LEFT: POSTER & ACTIONS */}
          <div className="details-poster-column">
            <div className="details-poster-wrap">
              <img 
                src={posterUrl} 
                alt={movie.title}
                className="details-poster-img"
                onError={(e) => {
                  e.target.src = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=600&auto=format&fit=crop";
                }}
              />
              {movie.trailer_key && (
                <button 
                  className="trailer-play-trigger"
                  onClick={() => setShowTrailerModal(true)}
                  aria-label="Play Trailer"
                >
                  <Play size={24} fill="#08090d" color="#08090d" />
                  <span>Preview Vision</span>
                </button>
              )}
            </div>

            {/* Quick Watchlist Action Card */}
            <div className="scholar-curation-box">
              <div className="curation-box-header">
                <Scroll size={18} className="curation-icon" />
                <h4>Scholar's Log</h4>
              </div>

              <div className="curation-status-selector">
                <label>Archive Status:</label>
                <div className="status-button-group">
                  <button 
                    type="button"
                    className={`status-chip ${status === 'plan_to_watch' ? 'selected' : ''}`}
                    onClick={() => setStatus('plan_to_watch')}
                  >
                    <Clock size={13} />
                    <span>Plan to Watch</span>
                  </button>

                  <button 
                    type="button"
                    className={`status-chip ${status === 'watching' ? 'selected' : ''}`}
                    onClick={() => setStatus('watching')}
                  >
                    <Eye size={13} />
                    <span>Studying</span>
                  </button>

                  <button 
                    type="button"
                    className={`status-chip ${status === 'completed' ? 'selected' : ''}`}
                    onClick={() => setStatus('completed')}
                  >
                    <Check size={13} />
                    <span>Completed</span>
                  </button>

                  <button 
                    type="button"
                    className={`status-chip ${status === 'favorite' ? 'selected' : ''}`}
                    onClick={() => setStatus('favorite')}
                  >
                    <Heart size={13} />
                    <span>Favorite</span>
                  </button>
                </div>
              </div>

              {/* Scholar Rating */}
              <div className="curation-rating-wrap">
                <label>Scholar Personal Rating:</label>
                <div className="star-rating-picker">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      key={star}
                      type="button"
                      className={`star-pick ${star <= scholarRating ? 'active' : ''}`}
                      onClick={() => setScholarRating(star === scholarRating ? 0 : star)}
                    >
                      <Star size={18} fill={star <= scholarRating ? "#f7df87" : "none"} color="#f7df87" />
                    </button>
                  ))}
                  <span className="rating-feedback">{scholarRating > 0 ? `${scholarRating * 2}/10` : 'Unrated'}</span>
                </div>
              </div>

              {/* Scholar Notes */}
              <div className="curation-notes-wrap">
                <label>Personal Scholar Notes & Insights:</label>
                <textarea
                  placeholder="Record your thoughts, symbolism, or historical significance..."
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  rows={3}
                ></textarea>
              </div>

              <div className="curation-actions">
                <button 
                  type="button" 
                  onClick={handleSaveWatchlist}
                  className="btn-ohara btn-ohara-primary curation-save-btn"
                >
                  <Bookmark size={16} />
                  <span>{inWatchlist ? "Update Archive Scroll" : "Add to Personal Watchlist"}</span>
                </button>

                {inWatchlist && (
                  <button 
                    type="button" 
                    onClick={handleRemove}
                    className="curation-remove-btn"
                  >
                    Remove from Watchlist
                  </button>
                )}
              </div>

              {notesSavedToast && (
                <div className="notes-toast animate-fade-in">
                  ✓ Recorded into your personal Ohara codex!
                </div>
              )}
            </div>
          </div>

          {/* RIGHT: INFO, CAST, OVERVIEW */}
          <div className="details-info-column">
            <div className="details-header-wrap">
              <div className="details-tagline">{movie.tagline || "Archived Cinematic Relic"}</div>
              <h1 className="details-title">{movie.title}</h1>
              
              <div className="details-badges-row">
                <div className="badge-gold">
                  <Star size={14} fill="#f7df87" />
                  <span>{rating} Score</span>
                </div>
                <span className="detail-meta-pill">
                  <Calendar size={13} />
                  {releaseYear}
                </span>
                {movie.runtime && (
                  <span className="detail-meta-pill">
                    <Clock size={13} />
                    {movie.runtime} min
                  </span>
                )}
                {movie.director && (
                  <span className="detail-meta-pill">
                    Director: <strong>{movie.director}</strong>
                  </span>
                )}
              </div>

              {/* Genres */}
              <div className="details-genres-list">
                {movie.genres && movie.genres.map((g) => (
                  <Link key={g.id || g} to={`/search?genre=${g.id || ''}`} className="genre-detail-pill">
                    {g.name || g}
                  </Link>
                ))}
              </div>
            </div>

            {/* Synopsis */}
            <div className="details-synopsis-section">
              <h3 className="section-title">
                <FileText size={18} />
                <span>Historical Synopsis</span>
              </h3>
              <p className="details-overview-text">
                {movie.overview || "No detailed synopsis recorded for this artifact."}
              </p>
            </div>

            {/* Cast List */}
            {movie.cast && movie.cast.length > 0 && (
              <div className="details-cast-section">
                <h3 className="section-title">
                  <User size={18} />
                  <span>Distinguished Cast & Figures</span>
                </h3>
                <div className="cast-grid-scroll">
                  {movie.cast.map((person, idx) => (
                    <div key={idx} className="cast-card">
                      <div className="cast-photo">
                        {person.profile_path ? (
                          <img src={getImageUrl(person.profile_path)} alt={person.name} loading="lazy" />
                        ) : (
                          <div className="cast-placeholder">
                            <User size={24} />
                          </div>
                        )}
                      </div>
                      <div className="cast-names">
                        <span className="actor-name">{person.name}</span>
                        <span className="character-name">{person.character || "Protagonist"}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Similar Movies */}
            {movie.similar && movie.similar.length > 0 && (
              <div className="details-similar-section">
                <h3 className="section-title">
                  <Sparkles size={18} />
                  <span>Related Ancient Chronicles</span>
                </h3>
                <div className="similar-movies-grid">
                  {movie.similar.slice(0, 4).map((sim) => (
                    <MovieCard key={sim.id} movie={sim} />
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* VIDEO TRAILER MODAL */}
      {showTrailerModal && movie.trailer_key && (
        <div className="trailer-modal-backdrop" onClick={() => setShowTrailerModal(false)}>
          <div className="trailer-modal-content" onClick={(e) => e.stopPropagation()}>
            <button 
              className="modal-close-btn" 
              onClick={() => setShowTrailerModal(false)}
              aria-label="Close modal"
            >
              <X size={24} />
            </button>
            <div className="video-iframe-wrapper">
              <iframe
                src={`https://www.youtube.com/embed/${movie.trailer_key}?autoplay=1`}
                title={`${movie.title} Trailer`}
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              ></iframe>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
import { useNavigate } from 'react-router-dom';
import { useWatchlist } from '../hooks/useWatchlist';
import { getImageUrl } from '../services/tmdb';
import { Star, Bookmark, Check, Calendar, Film } from 'lucide-react';
import './MovieCard.css';

export default function MovieCard({ movie }) {
  const navigate = useNavigate();
  const { isInWatchlist, toggleWatchlist } = useWatchlist();
  
  if (!movie) return null;

  const inWatchlist = isInWatchlist(movie.id);
  const year = movie.release_date ? movie.release_date.split('-')[0] : 'Ancient';
  const rating = movie.vote_average ? Number(movie.vote_average).toFixed(1) : 'N/A';
  const posterUrl = getImageUrl(movie.poster_path);

  const handleCardClick = () => {
    navigate(`/movie/${movie.id}`);
  };

  const handleWatchlistClick = (e) => {
    e.stopPropagation(); // prevent card navigation
    toggleWatchlist(movie);
  };

  return (
    <div className="ohara-movie-card" onClick={handleCardClick}>
      <div className="card-media-wrapper">
        <img 
          src={posterUrl} 
          alt={movie.title}
          loading="lazy"
          className="movie-card-poster"
          onError={(e) => {
            e.target.src = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=600&auto=format&fit=crop";
          }}
        />
        
        {/* Rating Badge */}
        <div className="card-badge rating-badge">
          <Star size={13} className="star-icon" fill="#f7df87" />
          <span>{rating}</span>
        </div>

        {/* Quick Watchlist Toggle */}
        <button 
          className={`card-bookmark-btn ${inWatchlist ? 'saved' : ''}`}
          onClick={handleWatchlistClick}
          title={inWatchlist ? "Remove from Watchlist" : "Add to Watchlist"}
          aria-label={inWatchlist ? "Remove from Watchlist" : "Add to Watchlist"}
        >
          {inWatchlist ? <Check size={16} /> : <Bookmark size={16} />}
        </button>

        {/* Hover Overlay */}
        <div className="card-hover-overlay">
          <div className="overlay-details">
            <span className="overlay-cta">Read Scroll &rarr;</span>
          </div>
        </div>
      </div>

      <div className="movie-card-info">
        <h3 className="movie-card-title" title={movie.title}>
          {movie.title}
        </h3>
        <div className="movie-card-meta">
          <span className="meta-year">
            <Calendar size={12} />
            {year}
          </span>
          {movie.genres && movie.genres.length > 0 && (
            <span className="meta-genre">
              {movie.genres[0].name || movie.genres[0]}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
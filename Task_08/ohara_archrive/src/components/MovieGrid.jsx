import MovieCard from './MovieCard';
import './MovieGrid.css';

export default function MovieGrid({ movies, title }) {
  if (!movies || movies.length === 0) {
    return (
      <div className="movie-grid-empty">
        <p>No movies found</p>
      </div>
    );
  }

  return (
    <div className="movie-grid-container">
      {title && <h2 className="movie-grid-title">{title}</h2>}
      <div className="movie-grid">
        {movies.map(movie => (
          <MovieCard key={movie.id} movie={movie} />
        ))}
      </div>
    </div>
  );
}

.movie-grid-container {
  padding: 20px;
}

.movie-grid-title {
  margin: 0 0 20px 0;
  font-size: 1.5rem;
  color: #fff;
  font-weight: 600;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
}

.movie-grid-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  color: #888;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .movie-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 15px;
  }
  
  .movie-grid-container {
    padding: 15px;
  }
}
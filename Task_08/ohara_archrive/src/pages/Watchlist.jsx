import { useWatchlist } from '../hooks/useWatchlist';
import MovieGrid from '../components/MovieGrid';
import { Link } from 'react-router-dom';
import './Watchlist.css';

export default function Watchlist() {
    const { watchlist } = useWatchlist();

    if (watchlist.length === 0) {
        return (
            <div className="watchlist-empty">
                <div className="empty-icon">🎬</div>
                <h2>Your watchlist is empty</h2>
                <p>Start exploring the archive and add movies you want to watch later.</p>
                <Link to="/search" className="explore-btn">Explore Movies</Link>
            </div>
        );
    }

    return (
        <div className="watchlist-page">
            <MovieGrid movies={watchlist} title="My Watchlist" />
        </div>
    );
}

.watchlist-page {
    padding: 2rem 8%;
    min-height: 80vh;
}

.watchlist-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 60vh;
    text-align: center;
    gap: 1rem;
}

.empty-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
}

.watchlist-empty h2 {
    color: #fff;
    font-size: 1.8rem;
    margin: 0;
}

.watchlist-empty p {
    color: #888;
    font-size: 1.1rem;
    max-width: 400px;
    margin: 0;
}

.explore-btn {
    margin-top: 1.5rem;
    padding: 0.8rem 1.5rem;
    background: #b5a8ff;
    color: #000;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.2s;
}

.explore-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(181, 168, 255, 0.3);
}

@media (max-width: 768px) {
    .watchlist-page {
        padding: 1.5rem 5%;
    }
}
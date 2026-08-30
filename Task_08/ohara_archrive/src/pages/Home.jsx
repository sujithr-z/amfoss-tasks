import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  getTrendingMovies,
  getPopularMovies,
  getTopRatedMovies,
  getUpcomingMovies,
  getGenres,
  getImageUrl
} from '../services/tmdb';
import { useWatchlist } from '../hooks/useWatchlist';
import MovieCard from '../components/MovieCard';
import SearchBar from '../components/SearchBar';
import Loading from '../components/Loading';
import ErrorMessage from '../components/ErrorMessage';
import { 
  Sparkles, 
  Flame, 
  Trophy, 
  Clock, 
  ChevronRight, 
  Bookmark, 
  Check, 
  Star, 
  Compass, 
  BookOpen, 
  ShieldCheck 
} from 'lucide-react';
import './Home.css';

export default function Home() {
  const [featured, setFeatured] = useState([]);
  const [activeSlide, setActiveSlide] = useState(0);
  const [genres, setGenres] = useState([]);
  
  const [mainMovies, setMainMovies] = useState([]);
  const [activeTab, setActiveTab] = useState('popular');
  
  const [sidebarTrending, setSidebarTrending] = useState([]);
  const [sidebarTopRated, setSidebarTopRated] = useState([]);
  const [sidebarUpcoming, setSidebarUpcoming] = useState([]);

  const [loading, setLoading] = useState(true);
  const [tabLoading, setTabLoading] = useState(false);
  const [error, setError] = useState(null);

  const { isInWatchlist, toggleWatchlist } = useWatchlist();

  useEffect(() => {
    const fetchHomeData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [trend, pop, top, upc, gen] = await Promise.all([
          getTrendingMovies(),
          getPopularMovies(),
          getTopRatedMovies(),
          getUpcomingMovies(),
          getGenres()
        ]);

        setFeatured(trend.slice(0, 5));
        setMainMovies(pop);
        setSidebarTrending(trend.slice(0, 5));
        setSidebarTopRated(top.slice(0, 5));
        setSidebarUpcoming(upc.slice(0, 5));
        setGenres(gen.slice(0, 14));
      } catch (err) {
        console.error("Home fetch error:", err);
        setError("Failed to load records from the Library of Ohara.");
      } finally {
        setLoading(false);
      }
    };

    fetchHomeData();
  }, []);

  // Automatic hero slider
  useEffect(() => {
    if (featured.length <= 1) return;
    const timer = setInterval(() => {
      setActiveSlide((prev) => (prev + 1) % featured.length);
    }, 7500);
    return () => clearInterval(timer);
  }, [featured.length]);

  const handleTabChange = async (tab) => {
    if (tab === activeTab) return;
    setActiveTab(tab);
    setTabLoading(true);
    try {
      let data = [];
      if (tab === 'popular') data = await getPopularMovies();
      else if (tab === 'trending') data = await getTrendingMovies();
      else if (tab === 'top_rated') data = await getTopRatedMovies();
      else if (tab === 'upcoming') data = await getUpcomingMovies();
      setMainMovies(data);
    } catch (e) {
      console.error(e);
    } finally {
      setTabLoading(false);
    }
  };

  if (loading) return <Loading message="Opening the sacred archives of Ohara..." />;
  if (error) return <ErrorMessage message={error} onRetry={() => window.location.reload()} />;

  const currentHero = featured[activeSlide] || featured[0];

  return (
    <div className="ohara-home-page">
      {/* HERO SECTION */}
      {currentHero && (
        <section className="ohara-hero-banner">
          <div 
            className="hero-backdrop" 
            style={{ 
              backgroundImage: `url(${getImageUrl(currentHero.backdrop_path || currentHero.poster_path, 'original')})` 
            }}
          >
            <div className="hero-gradient-overlay"></div>
          </div>

          <div className="hero-content-container">
            <div className="hero-badge-wrap">
              <span className="badge-gold">
                <Sparkles size={13} />
                ARCHIVE SPOTLIGHT
              </span>
              {currentHero.release_date && (
                <span className="hero-year">{currentHero.release_date.split('-')[0]}</span>
              )}
            </div>

            <h1 className="hero-movie-title">{currentHero.title}</h1>

            <div className="hero-meta-row">
              <span className="hero-rating">
                <Star size={16} fill="#f7df87" color="#f7df87" />
                <strong>{Number(currentHero.vote_average || 8).toFixed(1)}</strong>
              </span>
              {currentHero.runtime && (
                <span className="hero-runtime">
                  <Clock size={15} />
                  {currentHero.runtime} min
                </span>
              )}
              {currentHero.director && (
                <span className="hero-director">Dir: {currentHero.director}</span>
              )}
            </div>

            <p className="hero-overview-text">
              {currentHero.overview || "An extraordinary cinematic masterpiece preserved for posterity in the Library of Ohara."}
            </p>

            <div className="hero-action-buttons">
              <Link to={`/movie/${currentHero.id}`} className="btn-ohara btn-ohara-primary hero-btn">
                <BookOpen size={18} />
                <span>Examine Record</span>
              </Link>
              
              <button 
                className={`btn-ohara btn-ohara-secondary hero-btn ${isInWatchlist(currentHero.id) ? 'active' : ''}`}
                onClick={() => toggleWatchlist(currentHero)}
              >
                {isInWatchlist(currentHero.id) ? (
                  <>
                    <Check size={18} />
                    <span>In Watchlist</span>
                  </>
                ) : (
                  <>
                    <Bookmark size={18} />
                    <span>Save to Watchlist</span>
                  </>
                )}
              </button>
            </div>

            {/* Carousel Dots */}
            <div className="hero-carousel-dots">
              {featured.map((item, idx) => (
                <button
                  key={item.id}
                  className={`carousel-dot ${idx === activeSlide ? 'active' : ''}`}
                  onClick={() => setActiveSlide(idx)}
                  aria-label={`Slide ${idx + 1}`}
                >
                  <span className="dot-fill"></span>
                </button>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* QUICK SEARCH & SEARCH HERO */}
      <div className="home-search-container">
        <SearchBar />
      </div>

      {/* GENRES HORIZONTAL SCROLLER */}
      {genres.length > 0 && (
        <div className="genre-discovery-section">
          <div className="genre-scroll-wrapper">
            {genres.map((genre) => (
              <Link 
                key={genre.id} 
                to={`/search?genre=${genre.id}`}
                className="genre-tag-pill"
              >
                <span>{genre.name}</span>
              </Link>
            ))}
          </div>
        </div>
      )}

      {/* MAIN LAYOUT: ARCHIVE GRID & SIDEBAR SCHOLAR PICKS */}
      <div className="home-main-layout">
        <div className="home-content-column">
          {/* TABS HEADER */}
          <div className="archive-tabs-header">
            <div className="tabs-navigation">
              <button 
                className={`tab-btn ${activeTab === 'popular' ? 'active' : ''}`}
                onClick={() => handleTabChange('popular')}
              >
                <Flame size={16} />
                <span>Popular</span>
              </button>

              <button 
                className={`tab-btn ${activeTab === 'trending' ? 'active' : ''}`}
                onClick={() => handleTabChange('trending')}
              >
                <Sparkles size={16} />
                <span>Trending</span>
              </button>

              <button 
                className={`tab-btn ${activeTab === 'top_rated' ? 'active' : ''}`}
                onClick={() => handleTabChange('top_rated')}
              >
                <Trophy size={16} />
                <span>Top Rated</span>
              </button>

              <button 
                className={`tab-btn ${activeTab === 'upcoming' ? 'active' : ''}`}
                onClick={() => handleTabChange('upcoming')}
              >
                <Clock size={16} />
                <span>Upcoming</span>
              </button>
            </div>
          </div>

          {/* MOVIES GRID */}
          {tabLoading ? (
            <Loading message="Unrolling the selected scrolls..." />
          ) : (
            <div className="home-movies-grid">
              {mainMovies.map((movie) => (
                <MovieCard key={movie.id} movie={movie} />
              ))}
            </div>
          )}
        </div>

        {/* SIDEBAR */}
        <aside className="home-sidebar-column">
          {/* Sidebar Top Rated */}
          <SidebarRankList 
            title="Scholars' Masterpieces" 
            icon={<Trophy size={18} />} 
            movies={sidebarTopRated} 
            accent="#f7df87" 
          />

          {/* Sidebar Trending */}
          <SidebarRankList 
            title="Active Inquiries" 
            icon={<Flame size={18} />} 
            movies={sidebarTrending} 
            accent="#38bdf8" 
          />

          {/* Ohara Lore Box */}
          <div className="ohara-lore-card">
            <div className="lore-header">
              <ShieldCheck size={20} className="lore-icon" />
              <h4>Scholars' Creed</h4>
            </div>
            <p>
              "Books and cinema are the vessel of collective human memory. Even if an island is erased, the knowledge inscribed in our hearts will forever endure."
            </p>
            <div className="lore-author">— Tree of Knowledge, Ohara</div>
          </div>
        </aside>
      </div>
    </div>
  );
}

function SidebarRankList({ title, icon, movies, accent }) {
  if (!movies || movies.length === 0) return null;

  return (
    <div className="sidebar-rank-widget">
      <div className="rank-widget-header" style={{ borderLeftColor: accent }}>
        {icon}
        <h3>{title}</h3>
      </div>
      <div className="rank-items-list">
        {movies.map((movie, index) => (
          <Link to={`/movie/${movie.id}`} key={movie.id} className="rank-item-card">
            <div className="rank-number" style={{ color: index < 3 ? accent : 'var(--text-muted)' }}>
              0{index + 1}
            </div>
            <div className="rank-poster-thumb">
              <img src={getImageUrl(movie.poster_path)} alt={movie.title} loading="lazy" />
            </div>
            <div className="rank-info">
              <h5 className="rank-title">{movie.title}</h5>
              <div className="rank-meta">
                <span className="rank-rating">★ {Number(movie.vote_average || 0).toFixed(1)}</span>
                <span>•</span>
                <span>{movie.release_date ? movie.release_date.split('-')[0] : 'Relic'}</span>
              </div>
            </div>
            <ChevronRight size={16} className="rank-arrow" />
          </Link>
        ))}
      </div>
    </div>
  );
}
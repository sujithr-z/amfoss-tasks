import { useState, useEffect } from 'react';
import { NavLink, Link, useNavigate, useLocation } from 'react-router-dom';
import { useWatchlist } from '../hooks/useWatchlist';
import { Search, Bookmark, Compass, Film, BookOpen, Menu, X } from 'lucide-react';
import './Navbar.css';

export default function Navbar() {
  const { watchlist } = useWatchlist();
  const [navScrolled, setNavScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [navSearch, setNavSearch] = useState('');
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 30) {
        setNavScrolled(true);
      } else {
        setNavScrolled(false);
      }
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Close mobile menu on route change
  useEffect(() => {
    setMobileMenuOpen(false);
  }, [location.pathname]);

  const handleNavSearchSubmit = (e) => {
    e.preventDefault();
    if (navSearch.trim()) {
      navigate(`/search?q=${encodeURIComponent(navSearch.trim())}`);
      setNavSearch('');
    }
  };

  return (
    <header className={`ohara-navbar ${navScrolled ? 'scrolled' : ''}`}>
      <div className="navbar-container">
        {/* Brand */}
        <Link to="/" className="navbar-brand">
          <div className="brand-icon-wrapper">
            <span className="tree-emblem">🌳</span>
            <span className="scroll-emblem">📜</span>
          </div>
          <div className="brand-text">
            <span className="brand-title">OHARA ARCHIVE</span>
            <span className="brand-subtitle">LIBRARY OF CINEMA</span>
          </div>
        </Link>

        {/* Quick Search in Navbar */}
        <form onSubmit={handleNavSearchSubmit} className="nav-quick-search">
          <Search className="search-icon" size={16} />
          <input
            type="text"
            placeholder="Search the ancient scrolls..."
            value={navSearch}
            onChange={(e) => setNavSearch(e.target.value)}
            aria-label="Search movies"
          />
          {navSearch && (
            <button 
              type="button" 
              className="clear-search-btn"
              onClick={() => setNavSearch('')}
            >
              <X size={14} />
            </button>
          )}
        </form>

        {/* Desktop Navigation Links */}
        <nav className="navbar-links">
          <NavLink to="/" end className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            <Compass size={17} />
            <span>Discover</span>
          </NavLink>

          <NavLink to="/search" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            <Search size={17} />
            <span>Explore Grimoire</span>
          </NavLink>

          <NavLink to="/watchlist" className={({ isActive }) => `nav-link watchlist-link ${isActive ? 'active' : ''}`}>
            <Bookmark size={17} />
            <span>Watchlist</span>
            {watchlist.length > 0 && (
              <span className="watchlist-badge">{watchlist.length}</span>
            )}
          </NavLink>
        </nav>

        {/* Mobile Menu Toggle */}
        <button 
          className="mobile-menu-btn"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          aria-label="Toggle menu"
        >
          {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="mobile-drawer animate-fade-in">
          <form onSubmit={handleNavSearchSubmit} className="mobile-search">
            <Search size={18} />
            <input
              type="text"
              placeholder="Search movie scrolls..."
              value={navSearch}
              onChange={(e) => setNavSearch(e.target.value)}
            />
            <button type="submit" className="btn-ohara-primary mobile-search-btn">Go</button>
          </form>
          
          <div className="mobile-nav-links">
            <NavLink to="/" end className="mobile-link">
              <Compass size={20} />
              <span>Discover Archive</span>
            </NavLink>
            <NavLink to="/search" className="mobile-link">
              <Search size={20} />
              <span>Search Database</span>
            </NavLink>
            <NavLink to="/watchlist" className="mobile-link">
              <Bookmark size={20} />
              <span>Personal Watchlist</span>
              {watchlist.length > 0 && (
                <span className="watchlist-badge">{watchlist.length}</span>
              )}
            </NavLink>
          </div>
        </div>
      )}
    </header>
  );
}
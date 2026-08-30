import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Sparkles } from 'lucide-react';
import './SearchBar.css';

export default function SearchBar({ initialQuery = '', onSearch, placeholder = "Search the vast cinematic archives by title, scholar or director..." }) {
  const [query, setQuery] = useState(initialQuery);
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSearch) {
      onSearch(query.trim());
    } else if (query.trim()) {
      navigate(`/search?q=${encodeURIComponent(query.trim())}`);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="ohara-search-bar-form">
      <div className="search-bar-inner">
        <div className="search-icon-left">
          <Search size={22} />
        </div>
        <input
          type="text"
          className="search-input"
          placeholder={placeholder}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          aria-label="Search movies"
        />
        <button type="submit" className="search-submit-btn">
          <Sparkles size={16} />
          <span>Seek History</span>
        </button>
      </div>
    </form>
  );
}
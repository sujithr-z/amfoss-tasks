import { BookOpen } from 'lucide-react';
import './Loading.css';

export default function Loading({ message = "Consulting the ancient scrolls of Ohara..." }) {
  return (
    <div className="ohara-loading-container">
      <div className="loading-rune-wrapper">
        <div className="rune-ring-outer"></div>
        <div className="rune-ring-inner"></div>
        <BookOpen className="loading-book-icon" size={28} />
      </div>
      <p className="loading-text">{message}</p>
    </div>
  );
}
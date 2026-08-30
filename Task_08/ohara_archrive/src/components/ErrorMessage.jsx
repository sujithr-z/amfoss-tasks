import { AlertTriangle, RotateCcw } from 'lucide-react';
import './ErrorMessage.css';

export default function ErrorMessage({ 
  message = "An ancient obstruction prevented retrieval of this cinematic record.", 
  onRetry 
}) {
  return (
    <div className="ohara-error-container">
      <div className="error-icon-wrap">
        <AlertTriangle size={32} />
      </div>
      <h3 className="error-title">Archive Disruption</h3>
      <p className="error-description">{message}</p>
      {onRetry && (
        <button onClick={onRetry} className="btn-ohara btn-ohara-primary error-retry-btn">
          <RotateCcw size={16} />
          <span>Retry Retrieval</span>
        </button>
      )}
    </div>
  );
}
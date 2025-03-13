import React, { useState, useEffect } from 'react';
import { connect } from 'react-redux';
import agent from '../agent';

const RatingSubmission = ({ slug, currentUser }) => {
  const [ratingValue, setRatingValue] = useState(0);
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [existingRating, setExistingRating] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fetch user's existing rating when component mounts
  useEffect(() => {
    if (currentUser && slug) {
      setLoading(true);
      agent.Ratings.get(slug)
        .then(response => {
          const userRating = response.ratings.find(
            rating => rating.user.username === currentUser.username
          );
          if (userRating) {
            setExistingRating(userRating);
            setRatingValue(userRating.value);
          }
        })
        .catch(err => console.error('Error fetching ratings:', err))
        .finally(() => setLoading(false));
    }
  }, [slug, currentUser]);

  const handleSubmitRating = async () => {
    if (!currentUser) {
      setError('You must be logged in to submit a rating');
      return;
    }

    if (ratingValue < 1 || ratingValue > 5) {
      setError('Please select a rating from 1 to 5');
      return;
    }

    if (existingRating) {
      setError('You have already rated this item');
      return;
    }

    setSubmitting(true);
    setError(null);
    
    try {
      const response = await agent.Ratings.create(slug, { 
        rating: { value: ratingValue } 
      });
      setExistingRating(response.rating);
    } catch (err) {
      if (err.status === 409) {
        setError('You have already rated this item');
      } else {
        setError('Error submitting rating');
        console.error(err);
      }
    } finally {
      setSubmitting(false);
    }
  };

  if (!currentUser) {
    return null;
  }

  if (loading) {
    return (
      <div className="card mb-3">
        <div className="card-block p-3">
          <p>Loading rating information...</p>
        </div>
      </div>
    );
  }

  if (existingRating) {
    return (
      <div className="card mb-3">
        <div className="card-block p-3">
          <h4 className="card-title">Your Rating</h4>
          <div className="rating-stars mb-3">
            {[1, 2, 3, 4, 5].map(star => (
              <button 
                key={star}
                type="button"
                className={`btn ${existingRating.value >= star ? 'btn-primary' : 'btn-outline-secondary'} btn-sm me-1`}
                disabled={true}
                data-testid={`star-${star}`}
              >
                {star}
              </button>
            ))}
          </div>
          <p className="text-muted">You rated this item on {new Date(existingRating.created_at).toLocaleDateString()}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card mb-3">
      <div className="card-block p-3">
        <h4 className="card-title">Rate this item</h4>
        
        <div className="rating-stars mb-3">
          {[1, 2, 3, 4, 5].map(star => (
            <button 
              key={star}
              type="button"
              className={`btn ${ratingValue >= star ? 'btn-primary' : 'btn-outline-secondary'} btn-sm me-1`}
              onClick={() => setRatingValue(star)}
              data-testid={`star-${star}`}
            >
              {star}
            </button>
          ))}
        </div>

        {error && <div className="text-danger mb-2">{error}</div>}
        
        <button 
          className="btn btn-primary" 
          onClick={handleSubmitRating}
          disabled={submitting || ratingValue === 0}
          data-testid="submit-rating"
        >
          {submitting ? 'Submitting...' : 'Submit Rating'}
        </button>
      </div>
    </div>
  );
};

const mapStateToProps = state => ({
  currentUser: state.common.currentUser,
});

export default connect(mapStateToProps)(RatingSubmission);

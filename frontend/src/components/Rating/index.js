import React from 'react';

const Rating = ({ value, count }) => {
  // Convert value to number and handle invalid inputs
  const rating = parseFloat(value) || 0;
  
  // Generate stars based on rating value using Unicode characters
  const filledStar = '★';
  const emptyStar = '☆';
  
  const stars = [];
  for (let i = 1; i <= 5; i++) {
    stars.push(
      <span 
        key={i} 
        className={i <= rating ? "filled-star" : "empty-star"}
        style={{ color: i <= rating ? '#FFD700' : '#C0C0C0', fontSize: '1.25rem' }}
      >
        {i <= rating ? filledStar : emptyStar}
      </span>
    );
  }

  return (
    <div className="item-rating">
      <span className="mr-2">{stars}</span>
      <small className="text-muted ml-1">
        {rating.toFixed(1)} {count !== undefined && `(${count} ${count === 1 ? 'review' : 'reviews'})`}
      </small>
    </div>
  );
};

export default Rating;

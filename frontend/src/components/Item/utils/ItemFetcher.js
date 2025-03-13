import agent from "../../../agent";

export async function getItemAndComments(id) {
  const [item, comments, ratingsResponse] = await Promise.all([
    agent.Items.get(id),
    agent.Comments.forItem(id),
    agent.Ratings.get(id)
  ]);

  // Add rating data to the item
  if (ratingsResponse) {
    // Calculate average rating from ratings array
    let avgRating = 0;
    const ratingsCount = ratingsResponse.ratings_count || 
                         (ratingsResponse.ratings ? ratingsResponse.ratings.length : 0);
    
    // Calculate average if we have ratings
    if (ratingsResponse.ratings && ratingsResponse.ratings.length > 0) {
      const sum = ratingsResponse.ratings.reduce((acc, rating) => acc + rating.value, 0);
      avgRating = sum / ratingsResponse.ratings.length;
    }
    
    // Attach the rating data to the item
    item.item = {
      ...item.item,
      avgRating: avgRating,
      ratingsCount: ratingsCount
    };
  }

  return [item, comments];
}

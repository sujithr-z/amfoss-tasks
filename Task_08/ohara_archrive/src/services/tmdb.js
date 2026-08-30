export async function getTrendingMovies() {
    const data = await fetchTMDB(`/trending/movie/week`);
    return data.results;
}

export async function getUpcomingMovies() {
    const data = await fetchTMDB(`/movie/upcoming`);
    return data.results;
}

export async function getGenres() {
    const data = await fetchTMDB(`/genre/movie/list`);
    return data.genres;
}
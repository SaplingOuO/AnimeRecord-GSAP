import list from '../assets/MyProject/gamerAcg-List.json'

export const animesList = list;

export function getAnimeByYear(year) {
  return list
    .filter(item => item.releaseDate.startsWith(year + '年'))
    .sort((a, b) => new Date(b.releaseDate) - new Date(a.releaseDate));
}

export function getAllYears() {
  const years = new Set(list.map(item => item.releaseDate.slice(0, 4)));
  return Array.from(years).sort((a, b) => b - a);
}

export function getLatestYear(){
  return getAllYears()[0];
}
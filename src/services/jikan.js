import axios from 'axios'

export async function searchAnime(q, limit = 10) {
  try {
    const res = await axios.get('https://api.jikan.moe/v4/anime', {
      params: { q, limit }
    })
    return res.data?.data ?? []
  } catch (error) {
    console.error('Jikan API 錯誤:', error)
    return []
  }
}

export async function getYoutubeIdByName(name) {
  const list = await searchAnime(name, 1)
  const anime = list[0]
  // return anime?.trailer?.youtube_id ?? null
  return anime ?? null
}
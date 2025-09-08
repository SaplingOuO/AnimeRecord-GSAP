import axios from "axios"
let isAPILoaded = false
const API_KEY = "AIzaSyD9sXgoSgewLvfuPbX7BLUFtYk-md3m50c" //YouTube Data API Key

//載入 YouTube IFrame API (只會載入一次)
export function loadYoutubeAPI() {
  return new Promise((resolve) => {
    if (isAPILoaded && window.YT) {
      resolve(window.YT)
      return
    }

    const tag = document.createElement('script')
    tag.src = 'https://www.youtube.com/iframe_api'
    const firstScriptTag = document.getElementsByTagName('script')[0]
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag)

    window.onYouTubeIframeAPIReady = function () {
      isAPILoaded = true
      resolve(window.YT)
    }
  })
}

//檢查影片是否可播放 (用 YouTube Data API v3)
export async function checkYoutubeVideo(videoId) {
  try {
    const res = await axios.get("https://www.googleapis.com/youtube/v3/videos", {
      params: {
        part: "status,contentDetails",
        id: videoId,
        key: API_KEY,
        regionCode: "TW" 
      },
    })


    const video = res.data.items[0]
    const status = video.status
    const contentDetails = video.contentDetails
    const regionRestriction = contentDetails.regionRestriction

    if (res.data.items.length === 0) {
      return { playable: false, reason: "影片不存在或被刪除" }
    }
    if (status.uploadStatus !== "processed") {
      return { playable: false, reason: "影片尚未處理或被封鎖" }
    }
    if (status.privacyStatus !== "public") {
      return { playable: false, reason: "影片不是公開的" }
    }
    if (contentDetails.regionRestriction?.blocked) {
      return { playable: false, reason: "地區限制，無法播放" }
    }
    if (regionRestriction?.blocked?.includes("TW")) {
      return { playable: false, reason: "地區封鎖 (blocked)" }
    }
    if (regionRestriction?.allowed && !regionRestriction.allowed.includes("TW")) {
      return { playable: false, reason: "未允許在台灣播放 (allowed 限制)" }
    }

    return { playable: true, reason: "OK" }
  } catch (err) {
    console.error("YouTube Data API 錯誤:", err)
    return { playable: false, reason: "API 錯誤" }
  }
}

// 建立 YouTube 播放器（會先檢查影片是否可播）
export async function createYoutubePlayer(
  elementId,
  videoId,
  loopSwitch,
  muteSwitch,
  controlsSwitch,
  fsSwitch,
  disablekbSwitch,
) {
  // 先檢查影片狀態
  const check = await checkYoutubeVideo(videoId)
  if (!check.playable) {
    console.warn(`⚠️ 影片不可播放 (${videoId})，原因：${check.reason}`)
    return null
  }

  const YT = await loadYoutubeAPI()
  return new YT.Player(elementId, {
    height: '640',
    width: '360',
    videoId: videoId,
    playerVars: {
      playlist: videoId,           // 影片 ID（for loop）
      autoplay: 1,                 // 自動播放
      loop: loopSwitch,            // 循環播放
      mute: muteSwitch,            // 靜音（行動端自動播放通常需要靜音）
      controls: controlsSwitch,    // 顯示/隱藏控制列
      fs: fsSwitch,                // 顯示/隱藏全螢幕按鈕
      disablekb: disablekbSwitch,  // 禁止鍵盤控制
      playsinline: 1,              // 行動端內嵌播放
      rel: 0,                      // 結束時不顯示相關影片
      modestbranding: 1
    },
    events: {
      onReady: (event) => {
        event.target.playVideo()
      },
      onError: (error) => {
        console.error("⚠️ YouTube 播放錯誤:", error.data)
        // error.data 可能是：
        // 2: 無效參數
        // 5: HTML5 player 錯誤
        // 100: 影片移除或私密
        // 101, 150: 上傳者禁止在嵌入播放器播放
      }
    }
  })
}

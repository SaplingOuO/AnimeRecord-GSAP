let isAPILoaded = false

/**
 * 載入 YouTube IFrame API (只會載入一次)
 */
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

export async function createYoutubePlayer(
  elementId,
  videoId,
  loopSwitch,
  muteSwitch,
  controlsSwitch,
  fsSwitch,
  disablekbSwitch
) {
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
      }
    }
  })
}

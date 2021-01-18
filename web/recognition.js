/* eslint-disable no-new */
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)()

const translate = text => {
  return new Promise((resolve, reject) => {
    const e = document.createElement('div')
    e.textContent = text
    let i = 0
    const callback = () => {
      if (i++ === 4) resolve(e.textContent)
    }
    document.body.appendChild(e)
    e.addEventListener('DOMSubtreeModified', callback)
  })
}

// eslint-disable-next-line no-undef
googleTranslateElementInit = () => {
  // eslint-disable-next-line no-undef
  new google.translate.TranslateElement({
    pageLanguage: 'jp'
    // layout: google.translate.TranslateElement.InlineLayout.SIMPLE
  }, 'google_translate_element')
  setTimeout(() => {
    const e = document.querySelector('.goog-te-combo')
    e.value = 'en'
    e.dispatchEvent(new Event('change'))
    recognition.start()
  }, 1000)
}

const srtTimestamp = milliseconds => {
  let seconds = Math.round(milliseconds / 1000)
  // let milliseconds = seconds * 1000
  let minutes = Math.floor(seconds / 60)
  let hours = Math.floor(minutes / 60)
  milliseconds = milliseconds % 1000
  seconds = seconds % 60
  minutes = minutes % 60
  return (hours < 10 ? '0' : '') + hours + ':' +
    (minutes < 10 ? '0' : '') + minutes + ':' +
    (seconds < 10 ? '0' : '') + seconds + ',' +
    (milliseconds < 100 ? '0' : '') + (milliseconds < 10 ? '0' : '') + milliseconds
}

// recognition.continuous = true
recognition.interimResults = true
// let lasttime = new Date().getTime()

recognition.onstart = () => {
  console.debug('Recognition started')
}

let lasttime = new Date().getTime()
let lastSrt = srtTimestamp(0)
let index = 1

const send = async (text, translation) => {
  const current = new Date().getTime()
  const time = current - lasttime
  const srtTime = [lastSrt, srtTimestamp(time)]
  const res = await fetch('/transcript', {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      timestamp: Math.round(time / 1000),
      srtTime,
      text,
      translation,
      index: index++
    })
  })
  lasttime = current
  lastSrt = srtTime[1]
  return res
}

recognition.onresult = async (event) => {
  const result = event.results[event.results.length - 1]
  const resultText = Array.from(result).map(d => d.transcript).join('\n')
  console.debug(resultText)
  if (result.isFinal) {
    const resultTrans = await translate(resultText)
    console.log('%c {resultTrans}', 'font-size: x-large')
    await send(resultText, resultTrans)
  }
}

recognition.onspeechend = () => recognition.stop()

recognition.onerror = async e => {
  console.error('Error', e)
  // await send(' {e.error}:  {e.message}')
}

recognition.onend = () => {
  recognition.start()
}

recognition.lang = 'ja-JP'

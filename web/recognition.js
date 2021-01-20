/* eslint-disable no-new */

const THRESHOLD = 0.75

// const commonMistakes = {
//   '屋号': 'Yagoo'
// };

const fixMistakes = (text) => {
  // for (const item in text) {
  //   text.replaceAll(item, commonMistakes[item])
  // }
  return text
}

const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)()
const messagehistory = new Array(10)
let tlIndex = 0

const translate = text => {
  return new Promise((resolve, reject) => {
    const e = document.createElement('div')
    let i = (tlIndex + 1) % messagehistory.length
    while (i !== tlIndex) {
      const thistl = messagehistory[i]
      if (thistl) {
        e.innerHTML += `
          <span>${thistl}</span>
        `
      }
      i = (i + 1) % messagehistory.length
    }
    const tlelement = document.createElement('span')
    tlelement.textContent = text
    e.appendChild(tlelement)
    let lasttl = setTimeout(() => { }, 0)
    const callback = () => {
      const content = tlelement.textContent.replace(/[\u2018\u2019]/g, "'").replace(/[\u201C\u201D]/g, '"')
      clearTimeout(lasttl)
      lasttl = setTimeout(() => {
        messagehistory[tlIndex] = text
        tlIndex = (tlIndex + 1) % messagehistory.length
        e.remove()
        resolve(content)
      }, 1000)
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
  const hours = Math.floor(minutes / 60)
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

const begin = new Date().getTime()
let lastSrt = srtTimestamp(0)
let messageIndex = 1

const send = async (text, translation) => {
  const current = new Date().getTime()
  const time = current - begin
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
      tlIndex: messageIndex++
    })
  })
  lastSrt = srtTime[1]
  return res
}

let runningText = {
  text: '',
  num: 0
}

setInterval(() => {
  if (runningText.num === 0) return
  translate(runningText.text).then(async translation => {
    translation = translation.replaceAll('。', '.')
    console.log(`%c${translation}`, 'font-size: x-large')
    await send(runningText.text, translation)
  })
  runningText = {
    text: '',
    num: 0
  }
}, 15000)

recognition.onresult = async (event) => {
  const result = event.results[event.results.length - 1]
  const resultText = fixMistakes(Array.from(result).map(d => d.transcript).join('\n'))
  const confidence = result[0].confidence
  console.debug(resultText)
  if (result.isFinal) {
    if (confidence >= THRESHOLD) {
      runningText.text += resultText + '　'
      runningText.num++
    }
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

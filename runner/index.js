const puppeteer = require('puppeteer')
const fetch = require('node-fetch')

const machine = parseInt(process.argv[2])

async function main() {
  const browser = await puppeteer.launch({
    args: [
      '--use-fake-ui-for-media-stream',
      '--speech_recognition',
      '--enable-automation',
      '--autoplay-policy=no-user-gesture-required'
      // '--use-fake-device-for-media-stream'
    ],
    ignoreDefaultArgs: ['--mute-audio', '--disable-speech-api'],
    headless: false
  })
  const context = browser.defaultBrowserContext()
  const live = (await (await fetch('https://jetrico.sfo2.digitaloceanspaces.com/hololive/youtube.json')).json()).live
  if (machine >= live.length) {
    console.log('No stream to load')
    process.exit(0)
  }
  const stream = `https://www.youtube.com/watch?v=${live[machine].yt_video_key}`
  console.log(`Loading ${stream}`)
  await context.overridePermissions(stream, ['microphone'])
  const page = await browser.newPage()
  page.on('console', consoleObj => console.log(consoleObj.text()))
  const awaitingNav = page.waitForNavigation()
  await page.goto(stream)
  await awaitingNav
  setTimeout(async () => {
    await browser.close()
    process.exit(0)
  }, 60000)
}

main().catch(e => {
  console.error(e)
  process.exit(0)
})

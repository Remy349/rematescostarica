document.addEventListener('DOMContentLoaded', () => {
  const getRemainTime = (deadline) => {
    let now = new Date()
    let remainTime = (new Date(deadline) - now + 1000) / 1000
    let remainSeconds = ('0' + Math.floor(remainTime % 60)).slice(-2)
    let remainMinutes = ('0' + Math.floor((remainTime / 60) % 60)).slice(-2)
    let remainHours = ('0' + Math.floor((remainTime / 3600) % 24)).slice(-2)

    return {
      remainTime,
      remainSeconds,
      remainMinutes,
      remainHours,
    }
  }

  const countdown = (deadline, elem, finalMessage) => {
    const el = document.getElementById(elem)

    const timerUpdate = setInterval(() => {
      let time = getRemainTime(deadline)

      el.innerHTML = `La oferta termina en: ${time.remainHours}h:${time.remainMinutes}m:${time.remainSeconds}s`

      if (time.remainTime <= 1) {
        clearInterval(timerUpdate)
        el.innerHTML = finalMessage
      }
    }, 1000)
  }

  countdown(
    'Dec 31 2022 00:00:00 GMT-0600',
    'cuentaRegresiva',
    'Fin de la oferta!'
  )
})

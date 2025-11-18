const mqtt = require('mqtt')
const fetch = require('node-fetch')
const yargs = require('yargs/yargs')
const { hideBin } = require('yargs/helpers')

const argv = yargs(hideBin(process.argv))
  .option('api', { type: 'string', default: 'http://localhost:8000', description: 'Base URL da API' })
  .option('broker', { type: 'string', default: 'mqtt://localhost:1883', description: 'URL do broker MQTT' })
  .option('company', { type: 'number', demandOption: true, description: 'company_id' })
  .option('device', { type: 'string', demandOption: true, description: 'device_id' })
  .option('email', { type: 'string', demandOption: true, description: 'email para login' })
  .option('password', { type: 'string', demandOption: true, description: 'password para login' })
  .option('count', { type: 'number', default: 5, description: 'quantidade de mensagens a publicar' })
  .option('interval', { type: 'number', default: 1000, description: 'intervalo entre mensagens (ms)' })
  .argv

async function login(apiBase, email, password) {
  const url = `${apiBase.replace(/\/$/, '')}/login/`
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  })

  if (!res.ok) {
    throw new Error(`Login failed: ${res.status} ${res.statusText}`)
  }

  const body = await res.json()
  // body: { access: true, data: {...}, token: '...' }
  return body.token
}

async function run() {
  try {
    console.log('Simulator starting...')

    const token = await login(argv.api, argv.email, argv.password)
    console.log('Obtained token (length):', token ? token.length : 0)

    const clientId = `sim-${argv.company}-${argv.device}-${Math.floor(Math.random()*10000)}`

    const opts = {
      clientId: clientId,
      username: argv.email || clientId,
      password: token,
      reconnectPeriod: 1000
    }

    const client = mqtt.connect(argv.broker, opts)

    client.on('connect', () => {
      console.log('MQTT connected', argv.broker)

      const topic = `amemiya/${argv.company}/device/${argv.device}/telemetry`

      let sent = 0
      const timer = setInterval(() => {
        if (sent >= argv.count) {
          clearInterval(timer)
          client.end(true, () => {
            console.log('Done publishing, exiting')
            process.exit(0)
          })
          return
        }

        const payload = {
          version: '1.0',
          type: 'telemetry',
          company_id: argv.company,
          device_id: argv.device,
          ts: new Date().toISOString(),
          payload: {
            temperature: (20 + Math.random()*10).toFixed(2),
            battery: Math.floor(70 + Math.random()*30)
          }
        }

        client.publish(topic, JSON.stringify(payload), { qos: 1 }, (err) => {
          if (err) console.error('Publish error', err)
          else console.log(`Published ${++sent}/${argv.count} -> ${topic}`)
        })
      }, argv.interval)
    })

    client.on('error', (err) => {
      console.error('MQTT error', err)
    })

    client.on('close', () => {
      console.log('MQTT connection closed')
    })

  } catch (err) {
    console.error('Simulator error', err)
    process.exit(1)
  }
}

run()

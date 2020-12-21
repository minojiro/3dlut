import axios from 'axios'

const client = axios.create({
  baseURL: 'http://localhost:8000',
})

export async function generateFile(data) {
  const result = await client.post('calc', {data})
  return result.data
  // console.log(result)
  // const title = 'cube_test'
  // // const length = Math.pow(size, 3)
  // const floor6 = (f) => {
  //   return Math.min(Math.max(f, 0), 1)
  // }

  // const pointsstr = result.data.map(([r,g,b]) => `${floor6(r)} ${floor6(g)} ${floor6(b)}`)
  // return [
  //   '#Created by: Adobe Photoshop Export Color Lookup Plugin',
  //   `TITLE "${title}"`,
  //   '',
  //   '#LUT size',
  //   `LUT_3D_SIZE ${size}`,
  //   '',
  //   '#data domain',
  //   'DOMAIN_MIN 0.0 0.0 0.0',
  //   'DOMAIN_MAX 1.0 1.0 1.0',
  //   '',
  //   '#LUT data points',
  //   ...pointsstr,
  //   '\n',
  // ].join('\n')
}

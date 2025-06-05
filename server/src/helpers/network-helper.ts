import axios from 'axios'
import os from 'node:os'

const HUGGING_FACE_URL = 'https://huggingface.co'
const HUGGING_FACE_MIRROR_URL = 'https://hf-mirror.com'

export class NetworkHelper {
  /**
   * Check if the current network can access Hugging Face
   * @example canAccessHuggingFace() // true
   */
  public static async canAccessHuggingFace(): Promise<boolean> {
    try {
      await axios.head(HUGGING_FACE_URL)

      return true
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
    } catch (e) {
      return false
    }
  }

  /**
   * Set the Hugging Face URL based on the network access
   * @param url The URL to set
   * @example setHuggingFaceURL('https://huggingface.co') // https://hf-mirror.com
   */
  public static async setHuggingFaceURL(url: string): Promise<string> {
    const canAccess = await NetworkHelper.canAccessHuggingFace()

    if (!canAccess) {
      return url.replace(HUGGING_FACE_URL, HUGGING_FACE_MIRROR_URL)
    }

    return url
  }

  /**
   * Get the first non-internal IPv4 address
   * @example getLocalExternalIP() // '192.168.1.10'
   */
  public static getLocalExternalIP(): string | null {
    const nets = os.networkInterfaces()

    for (const name of Object.keys(nets)) {
      for (const net of nets[name] || []) {
        if (net.family === 'IPv4' && !net.internal) {
          return net.address
        }
      }
    }

    return null
  }
}

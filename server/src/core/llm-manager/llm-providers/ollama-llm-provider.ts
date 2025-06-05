import axios, { AxiosError } from 'axios'

import { LogHelper } from '@/helpers/log-helper'
import { CompletionParams } from '@/core/llm-manager/types'

export default class OllamaLLMProvider {
  protected readonly name = 'Ollama LLM Provider'
  private readonly model = process.env['OLLAMA_MODEL'] || 'mistral'
  private readonly axios = axios.create({
    baseURL: 'http://localhost:11434',
    timeout: 7000
  })

  constructor() {
    LogHelper.title(this.name)
    LogHelper.success('New instance')
  }

  public runChatCompletion(prompt: string, completionParams: CompletionParams): Promise<string> {
    return new Promise(async (resolve, reject) => {
      try {
        const messages: { role: string; content: string }[] = []
        if (completionParams.systemPrompt) {
          messages.push({ role: 'system', content: completionParams.systemPrompt })
        }
        if (completionParams.history) {
          for (const msg of completionParams.history) {
            messages.push({
              role: msg.who === 'leon' ? 'assistant' : 'user',
              content: msg.message
            })
          }
        }
        messages.push({ role: 'user', content: prompt })

        const resp = await this.axios.post('/api/chat', {
          model: this.model,
          messages,
          stream: false
        })
        resolve(resp.data.message.content as string)
      } catch (e) {
        const err = e as Error | AxiosError
        const errorMessage = `Failed to run completion: ${err}`
        LogHelper.title(this.name)
        LogHelper.error(errorMessage)
        reject(new Error(errorMessage))
      }
    })
  }
}

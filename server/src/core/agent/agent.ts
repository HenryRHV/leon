import fs from 'node:fs'

import { LogHelper } from '@/helpers/log-helper'
import { CustomLLMDuty } from '@/core/llm-manager/llm-duties/custom-llm-duty'
import { AGENT_MEMORY_PATH } from '@/constants'

export interface AgentStep {
  task: string
  tool?: string
}

export default class Agent {
  private readonly memoryPath = AGENT_MEMORY_PATH

  constructor() {
    LogHelper.title('Agent')
    LogHelper.success('New instance')

    if (!fs.existsSync(this.memoryPath)) {
      fs.writeFileSync(this.memoryPath, '[]', 'utf-8')
    }
  }

  private async loadMemory(): Promise<AgentStep[]> {
    try {
      const raw = await fs.promises.readFile(this.memoryPath, 'utf-8')
      return JSON.parse(raw) as AgentStep[]
    } catch (e) {
      LogHelper.error(`Failed to load agent memory: ${e}`)
    }

    return []
  }

  private async saveMemory(history: AgentStep[]): Promise<void> {
    try {
      await fs.promises.writeFile(
        this.memoryPath,
        JSON.stringify(history, null, 2),
        'utf-8'
      )
    } catch (e) {
      LogHelper.error(`Failed to save agent memory: ${e}`)
    }
  }

  private async addMemory(step: AgentStep): Promise<void> {
    const history = await this.loadMemory()
    history.push(step)
    await this.saveMemory(history)
  }

  public async plan(goal: string): Promise<AgentStep[]> {
    const duty = new CustomLLMDuty({
      input: `Break the following goal into steps in JSON array format: ${goal}`,
      data: { systemPrompt: 'You are a helpful planner that returns JSON.' }
    })
    await duty.init()
    const result = await duty.execute()

    try {
      const steps = JSON.parse(result?.output as unknown as string) as AgentStep[]
      return steps
    } catch (e) {
      LogHelper.error(`Failed to parse plan result: ${e}`)
    }

    return []
  }

  public async run(goal: string): Promise<AgentStep[]> {
    const plan = await this.plan(goal)
    for (const step of plan) {
      await this.addMemory(step)
    }
    return plan
  }
}

import fs from 'node:fs'
import path from 'node:path'
import JSZip from 'jszip'
import { parseStringPromise } from 'xml2js'
import { ChromaClient } from 'chromadb'

import { LogHelper } from '@/helpers/log-helper'
import { CustomLLMDuty } from '@/core/llm-manager/llm-duties/custom-llm-duty'

export interface MindMapNode {
  id: string
  title: string
  notes?: string
  children: MindMapNode[]
  summary?: string
  tags?: string[]
}

export class XMindIndexer {
  private chroma = new ChromaClient({})
  private collectionName: string
  private collection: Awaited<ReturnType<ChromaClient['getOrCreateCollection']>> | null = null

  constructor(collectionName = 'xmind') {
    this.collectionName = collectionName
  }

  private async ensureCollection(): Promise<void> {
    if (!this.collection) {
      this.collection = await this.chroma.getOrCreateCollection({
        name: this.collectionName
      })
    }
  }

  private parseTopic(xml: any): MindMapNode {
    const id = xml.$.id as string
    const title = Array.isArray(xml.title) ? xml.title[0] : ''
    const notes = xml.notes?.[0]?.plain?.[0] ?? ''

    const node: MindMapNode = { id, title, notes, children: [] }

    const childrenBlocks = xml.children?.[0]?.topics || []
    for (const block of childrenBlocks) {
      const topics = block.topic || []
      for (const child of topics) {
        node.children.push(this.parseTopic(child))
      }
    }

    return node
  }

  public async load(filePath: string): Promise<MindMapNode[]> {
    const buffer = await fs.promises.readFile(path.resolve(filePath))
    const zip = await JSZip.loadAsync(buffer)
    let content: string | null = null
    if (zip.files['content.json']) {
      content = await zip.files['content.json'].async('string')
      const json = JSON.parse(content)
      const sheets = json.sheets || []
      return sheets.map((s: any) => this.parseTopic(s.rootTopic))
    }

    if (zip.files['content.xml']) {
      content = await zip.files['content.xml'].async('string')
      const parsed = await parseStringPromise(content)
      const sheets = parsed['xmap-content'].sheet || []
      return sheets.map((s: any) => this.parseTopic(s.topic[0]))
    }

    throw new Error('Invalid XMind file')
  }

  private async summarizeNode(node: MindMapNode): Promise<void> {
    const duty = new CustomLLMDuty({
      input: `${node.title}\n${node.notes || ''}\nSummarize and provide tags as comma separated list`,
      data: { systemPrompt: 'You are a helpful assistant that summarizes mind map nodes and extracts tags.' }
    })
    await duty.init()
    const result = await duty.execute()
    if (result) {
      const out = String(result.output)
      const [summary, tags] = out.split('\n')
      node.summary = summary.trim()
      node.tags = (tags || '').split(',').map(t => t.trim()).filter(Boolean)
    }

    for (const child of node.children) {
      await this.summarizeNode(child)
    }
  }

  private flatten(node: MindMapNode, acc: MindMapNode[] = []): MindMapNode[] {
    acc.push(node)
    for (const child of node.children) {
      this.flatten(child, acc)
    }
    return acc
  }

  public async index(nodes: MindMapNode[]): Promise<void> {
    await this.ensureCollection()

    for (const node of nodes) {
      await this.summarizeNode(node)
      const flat = this.flatten(node)
      for (const item of flat) {
        const doc = `${item.title}\n${item.notes || ''}\n${item.summary || ''}`
        await this.collection?.add({
          ids: [item.id],
          documents: [doc]
        })
      }
    }
  }

  public async answer(question: string): Promise<string | null> {
    await this.ensureCollection()
    const res = await this.collection?.query({ queryTexts: [question], nResults: 3 })
    const docs = res?.documents?.[0] || []
    const context = docs.join('\n')
    const duty = new CustomLLMDuty({
      input: `Context:\n${context}\n\nQuestion: ${question}`,
      data: { systemPrompt: 'Answer the question based on the context.' }
    })
    await duty.init()
    const result = await duty.execute()
    return result ? String(result.output) : null
  }
}

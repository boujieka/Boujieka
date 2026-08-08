import "server-only";
import Anthropic from "@anthropic-ai/sdk";
import type { AIProvider, AIProviderMessage } from "./provider";

const DEFAULT_MODEL = "claude-sonnet-5";
const MAX_TOKENS = 1024;

export class AnthropicProvider implements AIProvider {
  private client: Anthropic;
  private model: string;

  constructor(apiKey: string, model: string = process.env.ANTHROPIC_MODEL ?? DEFAULT_MODEL) {
    this.client = new Anthropic({ apiKey });
    this.model = model;
  }

  async complete({
    system,
    messages,
  }: {
    system: string;
    messages: AIProviderMessage[];
  }): Promise<string> {
    const response = await this.client.messages.create({
      model: this.model,
      max_tokens: MAX_TOKENS,
      system,
      messages: messages.map((m) => ({ role: m.role, content: m.content })),
    });

    const textBlock = response.content.find((block) => block.type === "text");
    return textBlock?.type === "text" ? textBlock.text : "";
  }
}

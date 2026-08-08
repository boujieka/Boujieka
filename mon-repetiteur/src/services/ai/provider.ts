import "server-only";

export interface AIProviderMessage {
  role: "user" | "assistant";
  content: string;
}

/**
 * Provider-independent boundary (CLAUDE.md §7): application code never
 * imports an LLM SDK directly, only this interface. Swapping providers
 * means writing a new implementation of this file, nothing else.
 */
export interface AIProvider {
  complete(input: { system: string; messages: AIProviderMessage[] }): Promise<string>;
}

import { z } from "zod"

export const ZBlockType = z.enum(['round', 'square', 'triangle']);

export type BlockType = z.infer<typeof ZBlockType>;

import {z} from "zod"
import {ZBlockType} from './blocks-type';

export const ZBlock = z.object({
  id: z.number(),
  a: z.string(),
  b: z.number(),
  c: z.boolean(),
  block_type: ZBlockType,
});

export type Block = z.infer<typeof ZBlock>;

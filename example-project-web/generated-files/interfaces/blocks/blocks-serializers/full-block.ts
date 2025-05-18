import {z} from "zod";
import {ZBlockTypes} from "../../../enums/blocks/block-types";

export const ZFullBlock = z.object({
  id: z.number(),
  a: z.string(),
  b: z.number(),
  c: z.boolean(),
  block_type: ZBlockTypes,
  another_field: z.string(),
});

export type FullBlock = z.infer<typeof ZFullBlock>;

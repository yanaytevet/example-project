import {z} from "zod";
import {ZBlockTypes} from "../../../enums/blocks/block-types";
import {ZShortUser} from "../../users/user/short-user";

export const ZFullBlock = z.object({
  id: z.number(),
  a: z.string(),
  b: z.number(),
  c: z.boolean(),
  blockType: ZBlockTypes,
  anotherField: z.string(),
  user: ZShortUser,
});

export type FullBlock = z.infer<typeof ZFullBlock>;

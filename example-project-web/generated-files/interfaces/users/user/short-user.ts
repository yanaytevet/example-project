import {z} from "zod";


export const ZShortUser = z.object({
  id: z.number(),
  username: z.string(),
  full_name: z.string(),
  is_admin: z.boolean(),
});

export type ShortUser = z.infer<typeof ZShortUser>;

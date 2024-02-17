import {z} from "zod"


export const ZShortUser = z.object( {
  id: z.number(),
  username: z.string(),
  fullName: z.string(),
  isAdmin: z.boolean(),
});

export type ShortUser = z.infer<typeof ZShortUser>;
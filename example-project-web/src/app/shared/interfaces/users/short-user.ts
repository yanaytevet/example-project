import {z} from "zod"
import {ZPermission} from './permission';

export const ZShortUser = z.object({
  id: z.number(),
  username: z.string(),
  initials: z.string(),
  isAdmin: z.boolean(),
});

export type ShortUser = z.infer<typeof ZShortUser>;

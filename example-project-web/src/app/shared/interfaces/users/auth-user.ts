import { z } from "zod"
import {ZUser} from './user';

export const ZAuthUser = z.object({
  is_authenticated: z.boolean(),
  user: ZUser.nullable(),
  msg: z.string().nullable(),
});

export type AuthUser = z.infer<typeof ZAuthUser>;

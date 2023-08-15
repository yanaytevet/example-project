import { z } from "zod"
import {ZUser} from './user';

export const ZAuthUser = z.object({
  isAuthenticated: z.boolean(),
  user: ZUser.nullable(),
  msg: z.string().optional(),
});

export type AuthUser = z.infer<typeof ZAuthUser>;

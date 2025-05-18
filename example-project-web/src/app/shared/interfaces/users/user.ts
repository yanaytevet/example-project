import {z} from "zod"
import {ZPermission} from './permission';

export const ZUser = z.object({
  id: z.number(),
  username: z.string(),
  email: z.string().nullable(),
  first_name: z.string(),
  last_name: z.string(),
  pic_url: z.string().nullable(),
  permissions: z.array(ZPermission),
  full_name: z.string(),
  initials: z.string(),
  is_admin: z.boolean(),
});

export type User = z.infer<typeof ZUser>;

import {z} from "zod"
import {ZPermission} from './permission';

export const ZUser = z.object({
  id: z.number(),
  username: z.string(),
  email: z.string().nullable(),
  firstName: z.string(),
  lastName: z.string(),
  picUrl: z.string().nullable(),
  permissions: z.array(ZPermission),
  fullName: z.string(),
  initials: z.string(),
  isAdmin: z.boolean(),
});

export type User = z.infer<typeof ZUser>;

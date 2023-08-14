import { z } from "zod"

export const ZPermission = z.enum(['admin', 'editor']);

export type Permission = z.infer<typeof ZPermission>;

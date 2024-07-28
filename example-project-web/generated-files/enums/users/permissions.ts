import { z } from "zod"

export const ZPermissions = z.enum(["admin", "editor"]);

export type Permissions = z.infer<typeof ZPermissions>;

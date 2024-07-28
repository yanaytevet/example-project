import { z } from "zod"

export const ZTemporaryAccessType = z.enum(["reset_password"]);

export type TemporaryAccessType = z.infer<typeof ZTemporaryAccessType>;

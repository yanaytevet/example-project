import { z } from "zod"

export const ZEmailsValidationsTypes = z.enum(["none", "zerobounce"]);

export type EmailsValidationsTypes = z.infer<typeof ZEmailsValidationsTypes>;

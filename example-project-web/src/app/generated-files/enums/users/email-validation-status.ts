import { z } from "zod"

export const ZEmailValidationStatus = z.enum(["not_checked", "valid", "invalid", "catch_all", "unknown"]);

export type EmailValidationStatus = z.infer<typeof ZEmailValidationStatus>;


import { z } from "zod"

export const ZEmailsSendersTypes = z.enum(["none", "mandrill"]);

export type EmailsSendersTypes = z.infer<typeof ZEmailsSendersTypes>;

    
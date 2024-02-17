
import { z } from "zod"

export const ZBounceStatus = z.enum(["bounced", "did_not_bounce"]);

export type BounceStatus = z.infer<typeof ZBounceStatus>;

    
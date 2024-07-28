import { z } from "zod"

export const ZMarketingPlatformsTypes = z.enum(["none", "mailchimp"]);

export type MarketingPlatformsTypes = z.infer<typeof ZMarketingPlatformsTypes>;

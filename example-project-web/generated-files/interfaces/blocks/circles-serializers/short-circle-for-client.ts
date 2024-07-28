import {z} from "zod";


export const ZShortCircleForClient = z.object({
  id: z.number(),
});

export type ShortCircleForClient = z.infer<typeof ZShortCircleForClient>;

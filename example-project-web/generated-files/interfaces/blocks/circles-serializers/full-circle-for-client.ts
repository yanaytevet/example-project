import {z} from "zod";


export const ZFullCircleForClient = z.object({
  id: z.number(),
});

export type FullCircleForClient = z.infer<typeof ZFullCircleForClient>;

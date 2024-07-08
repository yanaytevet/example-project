import {z} from "zod";
import {ZShortUser} from "../../users/user/short-user";

export const ZFullCircleForClient = z.object({
  id: z.number(),
  user: ZShortUser,
});

export type FullCircleForClient = z.infer<typeof ZFullCircleForClient>;

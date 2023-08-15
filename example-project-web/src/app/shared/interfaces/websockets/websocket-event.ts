import {z} from "zod"

export const ZWebsocketEvent = z.object({
  eventType: z.string(),
  payload: z.any(),
});

export type WebsocketEvent = z.infer<typeof ZWebsocketEvent>;

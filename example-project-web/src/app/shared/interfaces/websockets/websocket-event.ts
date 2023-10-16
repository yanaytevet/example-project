import {z} from "zod"

export const ZWebsocketEvent = z.object({
  isConnectionEvent: z.boolean().optional(),
  actionHash: z.string().optional(),
  groupName: z.string(),
  eventType: z.string().optional(),
  payload: z.any().optional(),
});

export type WebsocketEvent = z.infer<typeof ZWebsocketEvent>;

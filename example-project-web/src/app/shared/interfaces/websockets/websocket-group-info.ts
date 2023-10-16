import {z} from "zod"

export const ZWebsocketGroupInfo = z.object({
  groupName: z.string(),
});

export type WebsocketGroupInfo = z.infer<typeof ZWebsocketGroupInfo>;

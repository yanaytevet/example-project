
import { z } from "zod"

export const ZStoragesTypes = z.enum(["none", "azure_storage"]);

export type StoragesTypes = z.infer<typeof ZStoragesTypes>;

    
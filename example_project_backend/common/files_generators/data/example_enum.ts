import { z } from "zod"

export const Zenum_name = z.enum(values_json);

export type enum_name = z.infer<typeof Zenum_name>;

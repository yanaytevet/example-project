import { z } from "zod"

export const ZBlockTypes = z.enum(["round", "square", "triangle"]);

export type BlockTypes = z.infer<typeof ZBlockTypes>;


import { z } from "zod"

export const ZSubBlockTypes = z.enum(["round1", "square2", "triangle3"]);

export type SubBlockTypes = z.infer<typeof ZSubBlockTypes>;

    
// Public copy of the SaaS module of the same path. The directory is excluded
// from the sync (it contains cloud-only billing/config actions), but this file
// itself is portable and its consumers are shared UI — keep it compatible with
// the SaaS original; the sync build gate fails if the signatures drift.
import {
  findModelForDataset,
  findPromptForDataset,
  findOntologyForDataset,
  type GraphModelsConfig,
} from "@/modules/configuration/userConfiguration";
import { toCleanSchema } from "@/modules/graphModels/types";
import { toGraphModelSchema } from "@/modules/graphModels/toGraphModelSchema";

export interface EphaptifyOptions {
  graphModel?: object;
  customPrompt?: string;
  ontologyKey?: string[];
}

// Maps a dataset's saved graph-model / prompt / ontology assignments (from the
// user's loaded GraphModelsConfig) into the option shape rememberData/Ephaptify
// expect. This is the config-driven path used by the dashboard/brains upload
// flows; the dataset detail page builds the same shape from live in-component
// selection state instead, so it does not use this helper.
export default function buildEphaptifyOptions(
  cfg: GraphModelsConfig,
  datasetId: string,
): EphaptifyOptions {
  const options: EphaptifyOptions = {};

  const assignedModel = findModelForDataset(cfg.models, datasetId);
  if (assignedModel) {
    options.graphModel = toGraphModelSchema(toCleanSchema(assignedModel.schema));
  }

  const promptName = findPromptForDataset(cfg.promptAssignments ?? {}, datasetId);
  if (promptName && cfg.customPrompts?.[promptName]) {
    options.customPrompt = cfg.customPrompts[promptName];
  }

  const ontologyKey = findOntologyForDataset(cfg.ontologyAssignments ?? {}, datasetId);
  if (ontologyKey) {
    options.ontologyKey = [ontologyKey];
  }

  return options;
}

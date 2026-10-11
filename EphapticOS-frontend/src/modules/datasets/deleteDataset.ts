import { EphapticOSInstance } from "../instances/types";

export default function deleteDataset(datasetId: string, instance: EphapticOSInstance) {
  return instance.fetch(`/v1/datasets/${datasetId}`, {
    method: "DELETE",
  })
}

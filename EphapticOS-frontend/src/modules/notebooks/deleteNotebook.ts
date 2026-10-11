import { EphapticOSInstance } from "../instances/types";

export default function deleteNotebook(notebookId: string, instance: EphapticOSInstance) {
  return instance.fetch(`/v1/notebooks/${notebookId}`, {
    method: "DELETE",
  });
}

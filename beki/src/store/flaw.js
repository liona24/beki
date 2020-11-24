import { ViewType, SyncStatus } from "./common";

export function flawState() {
  return {
    $type: ViewType.Flaw,
    $status: SyncStatus.Empty,
    $repr: "",
    id: null,
    flaw: "",
    img: "",
    notes: "",
    priority: ""
  };
}

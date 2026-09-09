import { Store } from "@app/store";
import { Store as Store2 } from "store";

export function boot(): Store {
  return new Store();
}

export function boot2(): Store2 {
  return new Store2();
}

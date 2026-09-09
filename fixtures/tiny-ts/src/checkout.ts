import { OrderService } from "./order.js";

export async function checkout(amount: number): Promise<string> {
  const svc = new OrderService();
  return svc.charge(amount);
}

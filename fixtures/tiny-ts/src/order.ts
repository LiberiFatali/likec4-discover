export class OrderService {
  async charge(amount: number): Promise<string> {
    return `charged:${amount}`;
  }
}

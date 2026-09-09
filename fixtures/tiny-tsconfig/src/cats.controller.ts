import { Controller, Get, Post, Body } from "@nestjs/common";

@Controller("cats")
export class CatsController {
  @Get()
  findAll(): string {
    return "cats";
  }

  @Post()
  create(@Body() body: unknown): unknown {
    return body;
  }
}

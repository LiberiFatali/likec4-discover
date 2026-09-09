const express = require("express");
const catchAsync = require("../utils/catchAsync");
const userController = require("./user.controller");

const router = express.Router();

router.get("/", (req, res) => res.send("ok"));

router
  .route("/:userId")
  .get(userController.getUser)
  .patch(userController.updateUser);

const createUser = catchAsync(async (req, res) => {
  res.send("created");
});

const plain = 42;

module.exports = { router, createUser };

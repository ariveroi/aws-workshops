#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { EcsCdkStack } from "../lib/ecs_cdk-stack";

const app = new cdk.App();

const env = {
  region: "eu-west-2",
  account: "145667828524",
  stackName:
    app.node.tryGetContext("stackName") ||
    process.env.STACK_NAME ||
    "AwsomeBuilderStack",
};

new EcsCdkStack(app, env.stackName, { env });

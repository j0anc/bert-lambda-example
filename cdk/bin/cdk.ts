#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { BERTLambdaStack } from '../lib/bert-lambda-stack';

const app = new cdk.App();
new BERTLambdaStack(app, 'BERTLambdaStack');
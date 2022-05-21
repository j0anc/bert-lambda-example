import { Stack, StackProps, Duration, CfnOutput } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from "aws-cdk-lib/aws-lambda"
import * as iam from "aws-cdk-lib/aws-iam"


export class BERTLambdaStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // define lambda function from docker image
    const bertFunction = new lambda.DockerImageFunction(this, "bert-function", {
      code: lambda.DockerImageCode.fromImageAsset("../"),
      memorySize: 3072,
      timeout: Duration.seconds(120),
      environment: {["S3_BUCKET_NAME"]: "bert-lambda-example-model-files"}
    })

    // create lambda function URL
    const lambdaUrl = bertFunction.addFunctionUrl({
      authType: lambda.FunctionUrlAuthType.NONE,
      cors:{
        allowedOrigins: ["*"]
      }
    })

    // create lambda iam policy for s3 access
    const s3Policy = new iam.PolicyStatement({
      resources: ["*"],
      actions: ["s3:*", "s3-object-lambda:*"]
    })

    // attach policy to lambda function
    bertFunction.role?.attachInlinePolicy(
      new iam.Policy(this, "s3Policy",{
        statements: [s3Policy]
      })
    )

    // output function URL after deployment
    new CfnOutput(this, "lambdaUrl", {
      value: lambdaUrl.url
    })


  }
}

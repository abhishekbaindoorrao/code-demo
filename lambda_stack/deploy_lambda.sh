if [[ -z "${DESTINATION_BUCKET}" ]]; then
   echo "No DESTINATION_BUCKET defined"
   exit 1
fi
zip lambda.zip lambda.py
# place lambda code for lambda to pickup
echo "Uploading code file to ${DESTINATION_BUCKET}"
aws s3 cp lambda.zip "s3://${DESTINATION_BUCKET}/lambda_code/lambda.zip"

echo "Deploying stack"
aws cloudformation deploy --stack-name lambda-antarctica --template-file lambda-antarctica.template --capabilities CAPABILITY_NAMED_IAM

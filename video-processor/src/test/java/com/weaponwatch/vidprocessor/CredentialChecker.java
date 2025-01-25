package com.weaponwatch.vidprocessor;

import software.amazon.awssdk.auth.credentials.DefaultCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.sts.StsClient;
import software.amazon.awssdk.services.sts.model.GetCallerIdentityResponse;
import software.amazon.awssdk.services.sts.model.StsException;

public class CredentialChecker {
    public static void main(String[] args) {
        try {
            StsClient stsClient = StsClient.builder()
                    .region(Region.US_EAST_1)
                    .credentialsProvider(DefaultCredentialsProvider.create())
                    .build();

            GetCallerIdentityResponse response = stsClient.getCallerIdentity();
            System.out.println("Your AWS Account: " + response.account());
            System.out.println("Your ARN: " + response.arn());
            System.out.println("You are logged in as: " + response.userId());

        } catch (StsException e) {
            System.err.println("Failed to retrieve identity.");
            e.printStackTrace();
        }
    }
}

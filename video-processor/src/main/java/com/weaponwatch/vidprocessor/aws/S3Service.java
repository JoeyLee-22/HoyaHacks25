package com.weaponwatch.vidprocessor.aws;

import software.amazon.awssdk.auth.credentials.DefaultCredentialsProvider;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.core.ResponseBytes;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;
import software.amazon.awssdk.services.s3.model.PutObjectResponse;
import software.amazon.awssdk.services.s3.model.GetObjectRequest;
import software.amazon.awssdk.services.s3.model.GetObjectResponse;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Paths;

public class S3Service {
    private final S3Client s3Client;

    public S3Service(){
        this.s3Client = S3Client.builder()
                .credentialsProvider(DefaultCredentialsProvider.create())
                .region(Region.US_EAST_1)
                .build();
    }

    public boolean uploadVideo(String bucketName, String objectKey, String filePath){
        try {
            PutObjectRequest request = PutObjectRequest.builder().bucket(bucketName).key(objectKey).build();
            PutObjectResponse response = s3Client.putObject(request, RequestBody.fromFile(new File(filePath)));
            return response.sdkHttpResponse().isSuccessful();
        }catch(Exception e) {
            e.printStackTrace();
            return false;
        }
    }
}

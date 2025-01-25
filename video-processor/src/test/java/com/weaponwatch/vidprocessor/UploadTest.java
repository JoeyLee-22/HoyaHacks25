package com.weaponwatch.vidprocessor;

import com.weaponwatch.vidprocessor.aws.S3Service;

import java.io.File;
import java.net.URISyntaxException;
import java.net.URL;

public class UploadTest {
    public static void main(String[] args) throws URISyntaxException {
        S3Service s3Service = new S3Service();
        String filePath = "C:\\Users\\chris\\IdeaProjects\\video-processor\\src\\test\\java\\com\\weaponwatch\\vidprocessor\\resources\\encryptIn\\9mm_fast_walk.mp4";
        try{
            s3Service.uploadVideo("weaponwatch-demo", "test-object1", filePath);
        }catch(Exception e){
            e.printStackTrace();
        }
    }
}

package com.weaponwatch.vidprocessor;

import com.weaponwatch.vidprocessor.encryption.EncryptionService;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;

public class EncryptionTest {
    public static void main(String[] args) throws IOException {
        String keyArn = "arn:aws:kms:us-east-1:203918845922:key/f0e18996-d4a0-49f6-827d-cc8915c5f864";
        EncryptionService encryptionService = new EncryptionService(keyArn);
        Path inPath = Paths.get("C:\\Users\\chris\\IdeaProjects\\video-processor\\src\\test\\java\\com\\weaponwatch\\vidprocessor\\resources\\encryptIn\\9mm_fast_walk.mp4");
        Path outPath = Paths.get("C:\\Users\\chris\\IdeaProjects\\video-processor\\src\\test\\java\\com\\weaponwatch\\vidprocessor\\resources\\encryptOut\\9mm.enc");
        encryptionService.encryptFile(inPath, outPath);
        System.out.println("Encrypted file to " + inPath);
    }
}

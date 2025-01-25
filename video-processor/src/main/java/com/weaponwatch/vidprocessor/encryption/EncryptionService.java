package com.weaponwatch.vidprocessor.encryption;

/*
    TODO: Excpetion Handling
 */

import com.amazonaws.encryptionsdk.AwsCrypto;
import com.amazonaws.encryptionsdk.CryptoResult;
import com.amazonaws.encryptionsdk.MasterKeyProvider;
import com.amazonaws.encryptionsdk.kms.KmsMasterKeyProvider;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Collections;


public class EncryptionService {
    private final AwsCrypto crypto;
    private final MasterKeyProvider<?> masterKeyProvider;

    public EncryptionService(String kmsKeyArn) {
        // Instantiate SDK
        this.crypto = AwsCrypto.builder().build();
        // Instantiate AWS KMS master key provider in strict mode using buildStrict().
        this.masterKeyProvider = KmsMasterKeyProvider.builder().buildStrict(kmsKeyArn);
    }

    public void encryptFile(Path inputPath, Path outputPath) throws IOException {
        byte[] plaintext = Files.readAllBytes(inputPath);
        /*TODO encryption context*/

        CryptoResult<byte[], ?> result = crypto.encryptData(masterKeyProvider, plaintext);
        final byte[] ciphertext = result.getResult();
        Files.write(outputPath, ciphertext);
    }

    public void decryptFile(Path inputPath, Path outputPath) throws IOException {
        byte[] ciphertext = Files.readAllBytes(inputPath);
        CryptoResult<byte[], ?> result = crypto.decryptData(masterKeyProvider, ciphertext);
        byte[] plaintext = result.getResult();
        Files.write(outputPath, plaintext);
    }
}

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.security.KeyFactory;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.SecureRandom;
import java.security.interfaces.RSAPrivateKey;
import java.security.interfaces.RSAPublicKey;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;
import java.util.UUID;
import javax.crypto.Cipher;


public class rsa {
    public static void main(String[] args) {

        String i = "hello world";
        System.out.println(i);
        /* 生成公私鑰 */
        KeyPairGenerator keyPairGenerator = null;
        try {
            keyPairGenerator = KeyPairGenerator.getInstance("RSA"); // NoSuchAlgorithmException
        } catch (Exception e) {
            e.printStackTrace();
        }
        keyPairGenerator.initialize(1024); // 此處可以新增引數new
                                           // SecureRandom(UUID.randomUUID().toString().getBytes())
        KeyPair keyPair = keyPairGenerator.generateKeyPair();
        RSAPublicKey rsaPublicKey = (RSAPublicKey) keyPair.getPublic();
        RSAPrivateKey rsaPrivateKey = (RSAPrivateKey) keyPair.getPrivate();

        try {
            Base64.Decoder decoder = Base64.getDecoder();
            Base64.Encoder encoder = Base64.getEncoder();
            String publicKeyString = encoder.encodeToString(rsaPublicKey.getEncoded());
            String privateKeyString = encoder.encodeToString(rsaPrivateKey.getEncoded());
            System.out.println(publicKeyString+"\n\n"+privateKeyString);
            KeyFactory keyFactory = KeyFactory.getInstance("RSA"); // NoSuchAlgorithmException

            byte[] keyBytes = decoder.decode(publicKeyString);
            X509EncodedKeySpec x509EncodedKeySpec = new X509EncodedKeySpec(keyBytes);
            RSAPublicKey p = (RSAPublicKey)keyFactory.generatePublic(x509EncodedKeySpec); // InvalidKeySepcException
            
            Cipher cipher = Cipher.getInstance("RSA"); //NoSuchPaddingException
            cipher.init(Cipher.ENCRYPT_MODE,p); //InvalidKeyException
            byte[] b = cipher.doFinal("12345678".getBytes()); //BadPaddingException
            System.out.println(new String(b));
        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}

package client;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class FileSyncClient {

    private static final String SERVER_URL = "http://127.0.0.1:5000"; // Flask 서버 주소
    private static final String MODS_DIR = "./mods"; // 로컬 mods 디렉터리
    private static final String CONFIGS_DIR = "./configs"; // 로컬 configs 디렉터리

    public static void main(String[] args) throws Exception {
        syncFiles("modslist", MODS_DIR);
        syncFiles("configslist", CONFIGS_DIR);
        System.out.println("Sync complete.");
    }

    private static void syncFiles(String listType, String localPath) throws Exception {
        System.out.println("Syncing " + listType + "...");

        // 디렉터리가 없으면 생성
        Path basePath = Paths.get(localPath);
        if (!Files.exists(basePath)) {
            System.out.println("Directory not found: " + localPath + ". Creating directory...");
            Files.createDirectories(basePath);
        }

        // 서버에서 디렉터리 트리 가져오기
        String url = SERVER_URL + "/api/" + listType;
        String jsonResponse = sendGetRequest(url);
        Gson gson = new Gson();
        Map<String, Map<String, List<String>>> serverTree = gson.fromJson(jsonResponse, new TypeToken<Map<String, Map<String, List<String>>>>() {}.getType());

        // 로컬 디렉터리 트리 생성
        Map<String, Map<String, List<String>>> localTree = buildLocalTree(Paths.get(localPath));

        // 서버와 로컬 비교 후 변경된 파일 다운로드
        for (String relativePath : serverTree.keySet()) {
            Map<String, List<String>> serverFiles = serverTree.get(relativePath);
            List<String> serverFileList = serverFiles.get("files");

            Path localDir = Paths.get(localPath, relativePath);
            if (!Files.exists(localDir)) {
                Files.createDirectories(localDir);
            }

            for (String fileName : serverFileList) {
                Path localFile = localDir.resolve(fileName);
                String serverHash = sendGetRequest(getCleanPath(SERVER_URL + "/api/hash/" + relativePath + "/" + fileName));

                if (!Files.exists(localFile) || !serverHash.equals(hashFile(localFile))) {
                    System.out.println(getCleanPath("Downloading: " + relativePath + "/" + fileName));
                    downloadFile(getCleanPath(SERVER_URL + "/api/download/" + relativePath + "/" + fileName), localFile.toString());
                }
            }
        }
    }

    private static String getCleanPath(String path) throws Exception {
        // 경로에서 .을 포함하지 않도록 처리 (예: './' -> '')
        return path.replace("./", "");
    }

    private static String sendGetRequest(String urlString) throws IOException {
        URL url = new URL(urlString);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");

        try (BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()))) {
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                response.append(line);
            }
            return response.toString();
        }
    }

    private static void downloadFile(String urlString, String savePath) throws IOException {
        URL url = new URL(urlString);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");

        try (InputStream in = connection.getInputStream();
             OutputStream out = new FileOutputStream(savePath)) {
            byte[] buffer = new byte[1024];
            int bytesRead;
            while ((bytesRead = in.read(buffer)) != -1) {
                out.write(buffer, 0, bytesRead);
            }
        }
    }

    private static String hashFile(Path filePath) throws Exception {
        MessageDigest digest = MessageDigest.getInstance("SHA-256");

        try (InputStream fis = Files.newInputStream(filePath)) {
            byte[] buffer = new byte[1024];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                digest.update(buffer, 0, bytesRead);
            }
        }

        byte[] hashBytes = digest.digest();
        StringBuilder hashString = new StringBuilder();
        for (byte b : hashBytes) {
            hashString.append(String.format("%02x", b));
        }
        return hashString.toString();
    }

    private static Map<String, Map<String, List<String>>> buildLocalTree(Path basePath) throws IOException {
        Map<String, Map<String, List<String>>> tree = new HashMap<>();

        Files.walk(basePath).forEach(path -> {
            if (Files.isDirectory(path)) {
                String relativePath = basePath.relativize(path).toString();
                try (DirectoryStream<Path> stream = Files.newDirectoryStream(path)) {
                    Map<String, List<String>> entry = new HashMap<>();
                    entry.put("dirs", Files.list(path)
                            .filter(Files::isDirectory)
                            .map(p -> p.getFileName().toString())
                            .toList());
                    entry.put("files", Files.list(path)
                            .filter(Files::isRegularFile)
                            .map(p -> p.getFileName().toString())
                            .toList());
                    tree.put(relativePath, entry);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });
        return tree;
    }
}

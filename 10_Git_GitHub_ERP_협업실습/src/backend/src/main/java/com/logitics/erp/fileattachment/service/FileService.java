package com.logitics.erp.fileattachment.service;

import com.logitics.erp.fileattachment.entity.FileAttachment;
import com.logitics.erp.fileattachment.repository.FileAttachmentRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.core.io.UrlResource;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class FileService {

    private final FileAttachmentRepository fileAttachmentRepository;

    public Long upload(MultipartFile file, String refType, Long refId) throws Exception {
        // 1. 원본 파일명
        String originalName = file.getOriginalFilename();

        // 2. 확장자 추출
        String extension = originalName.substring(originalName.lastIndexOf(".") + 1);

        // 3. 저장 파일명
        String storedName = UUID.randomUUID() + "." + extension;

        // 4. 저장 경로
//        Path uploadPath = Paths.get("./uploads");
        Path uploadPath = Paths.get(System.getProperty("user.dir"), "uploads");

        if (!Files.exists(uploadPath)) {
            Files.createDirectories(uploadPath);
        }

        // 5. 실제 파일 저장
        Path filePath = uploadPath.resolve(storedName);
        file.transferTo(filePath.toFile());

        // 6. DB 저장
        FileAttachment fileAttachment = new FileAttachment();
        fileAttachment.setRefType(refType);
        fileAttachment.setRefId(refId);
        fileAttachment.setOriginalName(originalName);
        fileAttachment.setStoredName(storedName);
        fileAttachment.setFilePath(filePath.toString());
        fileAttachment.setExtension(extension);
        fileAttachment.setContentType(file.getContentType());
        fileAttachment.setFileSize(file.getSize());

        fileAttachmentRepository.save(fileAttachment);

        return fileAttachment.getFileId();
    }

    public ResponseEntity<Resource> download(Long fileId) throws Exception {

        FileAttachment file = fileAttachmentRepository.findById(fileId)
                .orElseThrow(() -> new RuntimeException("파일 정보가 없습니다."));

        Path path = Paths.get(file.getFilePath());
        Resource resource = new UrlResource(path.toUri());

        if (!resource.exists()) {
            throw new RuntimeException("파일이 존재하지 않습니다.");
        }

        String encodedFileName = URLEncoder.encode(
                file.getOriginalName(),
                StandardCharsets.UTF_8
        ).replaceAll("\\+", "%20");

        return ResponseEntity.ok()
                .header(
                        HttpHeaders.CONTENT_DISPOSITION,
                        "attachment; filename*=UTF-8''" + encodedFileName
                )
                .contentType(MediaType.APPLICATION_OCTET_STREAM)
                .body(resource);
    }

}

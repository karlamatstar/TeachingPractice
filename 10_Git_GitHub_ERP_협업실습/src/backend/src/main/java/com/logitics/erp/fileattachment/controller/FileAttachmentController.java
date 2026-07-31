package com.logitics.erp.fileattachment.controller;

import com.logitics.erp.fileattachment.service.FileService;
import io.swagger.v3.oas.annotations.Operation;
import lombok.RequiredArgsConstructor;
import org.springframework.core.io.Resource;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/v1/files")
@RequiredArgsConstructor
public class FileAttachmentController {

    private final FileService fileService;

    @PostMapping("/upload")
    @Operation(description = "refId")
    public Long uploadFile(
            @RequestParam("file") MultipartFile file,
            @RequestParam("refType") String refType
//            @RequestParam("refId") Long refId
    ) throws  Exception{
        Long refId = 0L;
        Long fileId = fileService.upload(file, refType, refId);
        return fileId;
    }

    @GetMapping("/{fileId}/download")
    public ResponseEntity<Resource> download(@PathVariable Long fileId) throws Exception{
        return fileService.download(fileId);
    }
}

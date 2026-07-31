package com.logitics.erp.fileattachment.repository;

import com.logitics.erp.fileattachment.entity.FileAttachment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface FileAttachmentRepository extends JpaRepository<FileAttachment, Long> {
}

package com.logitics.erp.employeecertificateissue.mapper;

import com.logitics.erp.employeecertificateissue.dto.EmployeeCertificateIssueResponse;

import java.util.List;

public interface EmployeeCertificateIssueMapper {
	List<EmployeeCertificateIssueResponse> getCertificateIssue(Long myEmployeeId, int offset, int size);
}

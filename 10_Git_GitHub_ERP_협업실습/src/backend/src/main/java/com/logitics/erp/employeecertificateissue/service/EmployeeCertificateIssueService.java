package com.logitics.erp.employeecertificateissue.service;

import com.logitics.erp.employeecertificateissue.dto.EmployeeCertificateIssueResponse;
import com.logitics.erp.employeecertificateissue.mapper.EmployeeCertificateIssueMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class EmployeeCertificateIssueService {

	private final EmployeeCertificateIssueMapper employeeCertificateIssueMapper;

	public List<EmployeeCertificateIssueResponse> getCertificateIssue(
					Long myEmployeeId,
					int size,
					int page
	) {
		int offset = page * 10;
		return employeeCertificateIssueMapper.getCertificateIssue(myEmployeeId, offset, size);
	}

}

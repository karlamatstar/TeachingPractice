package com.logitics.erp.employeecertificateissue.controller;

import com.logitics.erp.employeecertificateissue.dto.EmployeeCertificateIssueResponse;
import com.logitics.erp.employeecertificateissue.service.EmployeeCertificateIssueService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/certificateIssue")
public class EmployeeCertificateIssueController {

	private final EmployeeCertificateIssueService employeeCertificateIssueService;

	@GetMapping
	public List<EmployeeCertificateIssueResponse> getCertificateIssue(
					@RequestParam Long myEmployeeId,
					@RequestParam int page,
					@RequestParam int size
	) {
		return employeeCertificateIssueService.getCertificateIssue(myEmployeeId, page, size);
	}

}

package com.logitics.erp.employeecertificate.controller;

import java.util.List;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.logitics.erp.employeecertificate.dto.EmployeeCertificateAddInfoRequest;
import com.logitics.erp.employeecertificate.dto.EmployeeCertificateInfoResponse;
import com.logitics.erp.employeecertificate.service.EmployeeCertificateService;

import io.swagger.v3.oas.annotations.Operation;
import lombok.RequiredArgsConstructor;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/certificate")
public class EmployeeCertificateController {

	private final EmployeeCertificateService employeeCertificateService;

	@GetMapping
	@Operation(summary = "자격증 조회", description = "직원 자격증 조회")
	public List<EmployeeCertificateInfoResponse> getEmployeeCertificateInfo(
					@RequestParam Long employeeId
	) {
		return employeeCertificateService.getEmployeeCertificateInfo(employeeId);
	}

	@PostMapping
	@Operation(summary = "자격증 추가", description = "직원 자격증 정보 추가")
	public boolean addInfo(
					@RequestBody EmployeeCertificateAddInfoRequest addRequest
	) {
		return employeeCertificateService.addCertificateInfo(addRequest);
	}

	@DeleteMapping("/{certificateId}")
	@Operation(summary = "자격증 삭제", description = "직원 자격증 정보 삭제")
	public boolean deleteInfo(
					@PathVariable Long certificateId
	) {
		return employeeCertificateService.deleteCertificateInfo(certificateId);
	}
}
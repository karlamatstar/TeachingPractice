package com.logitics.erp.employeecareer.controller;

import com.logitics.erp.employeecareer.dto.EmployeeCareerAddInfoRequest;
import com.logitics.erp.employeecareer.dto.EmployeeCareerInfoResponse;
import com.logitics.erp.employeecareer.service.EmployeeCareerService;
import io.swagger.v3.oas.annotations.Operation;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/career")
public class EmployeeCareerController {

	private final EmployeeCareerService employeeCareerService;

	@GetMapping
	public List<EmployeeCareerInfoResponse> getEmployeeCareerInfo(@RequestParam Long employeeId) {
		return employeeCareerService.getEmployeeCareerInfo(employeeId);
	}

	@PostMapping
	@Operation(summary = "경력 추가", description = "직원 경력 정보 추가")
	public boolean addInfo(
					@RequestBody EmployeeCareerAddInfoRequest addRequest
	) {
		return employeeCareerService.addInfo(addRequest);
	}
	@DeleteMapping("/{careerId}")
	@Operation(summary = "경력 삭제", description = "직원 경력 정보 삭제")
	public boolean deleteInfo(
					@PathVariable Long careerId
	) {
		return employeeCareerService.deleteInfo(careerId);
	}

}

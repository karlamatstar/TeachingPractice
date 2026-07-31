package com.logitics.erp.employeeeducation.controller;

import com.logitics.erp.employeeeducation.dto.EmployeeEducationInfoRequest;
import com.logitics.erp.employeeeducation.dto.EmployeeEducationInfoResponse;
import com.logitics.erp.employeeeducation.entity.EmployeeEducation;
import com.logitics.erp.employeeeducation.service.EmployeeEducationService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/education")
public class EmployeeEducationController {

	private final EmployeeEducationService employeeEducationService;

	@GetMapping
	public List<EmployeeEducationInfoResponse> getEmployeeEducationInfo(String employeeNo) {
		return employeeEducationService.getEmployeeEducationInfo(employeeNo);
	}

	@PostMapping
	public boolean addEmployeeEducationInfo(@RequestBody EmployeeEducationInfoRequest educationInfoRequest) {
		return employeeEducationService.addEmployeeEducationInfo(educationInfoRequest);
	}

	@DeleteMapping("/{educationId}")
	public boolean deleteEmployeeEducationInfo(@PathVariable Long educationId) {
		return employeeEducationService.deleteEmployeeEducationInfo(educationId);
	}

}

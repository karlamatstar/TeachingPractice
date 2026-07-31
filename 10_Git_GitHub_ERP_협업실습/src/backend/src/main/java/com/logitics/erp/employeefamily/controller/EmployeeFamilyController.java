package com.logitics.erp.employeefamily.controller;

import com.logitics.erp.employeefamily.dto.EmployeeFamilyInfoRequest;
import com.logitics.erp.employeefamily.dto.EmployeeFamilyInfoResponse;
import com.logitics.erp.employeefamily.service.EmployeeFamilyService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/family")
@RequiredArgsConstructor
public class EmployeeFamilyController {

	private final EmployeeFamilyService familyService;

	@GetMapping
	public List<EmployeeFamilyInfoResponse> getEmployeeFamilyInfo(@RequestParam(required = false) String employeeNo) {
		return familyService.getEmployeeFamilyInfo(employeeNo);
	}

	@PostMapping
	public boolean addFamilyInfo(@RequestBody EmployeeFamilyInfoRequest familyInfoRequest) {
		return familyService.addFamiliyInfo(familyInfoRequest);
	}

	@DeleteMapping("/{familyId}")
	public boolean deleteFamilyInfo(@PathVariable Long familyId) {
		return familyService.deleteFamilyInfo(familyId);
	}

}

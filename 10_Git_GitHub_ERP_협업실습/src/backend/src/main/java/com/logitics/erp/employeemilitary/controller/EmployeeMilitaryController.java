package com.logitics.erp.employeemilitary.controller;

import com.logitics.erp.employeemilitary.dto.EmployeeMilitaryInfoResponse;
import com.logitics.erp.employeemilitary.dto.EmployeeMilitaryAddInfoRequest;
import com.logitics.erp.employeemilitary.service.EmployeeMilitaryService;
import io.swagger.v3.oas.annotations.Operation;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/military")
public class EmployeeMilitaryController {

	private final EmployeeMilitaryService employeeMilitaryService;

	@GetMapping
	public List<EmployeeMilitaryInfoResponse> getEmployeeMilitaryInfo(@RequestParam String employeeNo) {
		return employeeMilitaryService.getEmployeeMilitaryInfo(employeeNo);
	}

	@PostMapping
	@Operation(summary = "병역정보 추가", description = "직원 병역 정보 추가")
	public boolean addMilitaryInfo(
					@RequestBody EmployeeMilitaryAddInfoRequest addRequest
	) {
		return employeeMilitaryService.addMilitaryInfo(addRequest);
	}

	@DeleteMapping("/{certificateId}")
	@Operation(summary = "병역정보 삭제", description = "직원 병역 정보 삭제")
	public boolean deleteInfo(
					@PathVariable Long militaryId
	) {
		return employeeMilitaryService.deleteMilitaryInfo(militaryId);
	}

}

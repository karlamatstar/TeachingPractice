package com.logitics.erp.employeelanguage.controller;

import com.logitics.erp.employeelanguage.dto.EmployeeLanguageInfoRequest;
import com.logitics.erp.employeelanguage.dto.EmployeeLanguageInfoResponse;
import com.logitics.erp.employeelanguage.service.EmployeeLanguageService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/employeeLanguage")
public class EmployeeLanguageController {

	private final EmployeeLanguageService employeeLanguageService;

	@GetMapping
	public List<EmployeeLanguageInfoResponse> getEmployeeLanguageInfo(@RequestParam String employNo) {
		return employeeLanguageService.getEmployeeLanguageInfo(employNo);
	}

	@PostMapping
	public boolean addEmployeeLanguageInfo(@RequestBody EmployeeLanguageInfoRequest languageInfoRequest) {
		return employeeLanguageService.addEmployeeLanguageInfo(languageInfoRequest);
	}

	@DeleteMapping("/{languageId}")
	public boolean deleteEmployeeLanguageInfo(@PathVariable Long languageId) {
		return employeeLanguageService.deleteEmployeeLanguageInfo(languageId);
	}

}

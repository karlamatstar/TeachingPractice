package com.logitics.erp.employeeallowance.controller;

import com.logitics.erp.employeeallowance.dto.EmployeeAllowanceStandardResponse;
import com.logitics.erp.employeeallowance.service.EmployeeAllowanceService;
import io.swagger.v3.oas.annotations.Operation;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/employeeAllowance")
public class EmployeeAllowanceController {

	private final EmployeeAllowanceService employeeAllowanceService;


}

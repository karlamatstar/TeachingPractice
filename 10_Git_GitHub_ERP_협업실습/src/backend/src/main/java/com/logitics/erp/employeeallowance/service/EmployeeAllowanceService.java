package com.logitics.erp.employeeallowance.service;

import com.logitics.erp.employeeallowance.dto.EmployeeAllowanceStandardResponse;
import com.logitics.erp.employeeallowance.mapper.EmployeeAllowanceMapper;
import com.logitics.erp.employeeallowance.repository.EmployeeAllowanceRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;

@Service
@RequiredArgsConstructor
public class EmployeeAllowanceService {
	private final EmployeeAllowanceRepository allowanceRepository;
	private final EmployeeAllowanceMapper allowanceMapper;

}

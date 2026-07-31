package com.logitics.erp.employeeallowance.dto;

import com.logitics.erp.employee.entity.Employee;
import jakarta.persistence.*;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDate;

@Data
public class EmployeeAllowanceStandardResponse {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long employeeAllowanceId;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "employee_id")
	private Employee employee;

	private Long allowanceId;
	private BigDecimal amount;

	private LocalDate startDate;
	private LocalDate endDate;
}
